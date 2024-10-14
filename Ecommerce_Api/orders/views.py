from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from products.models import Product
from .serializers import OrderSerializer
from django.db import transaction
from rest_framework.views import APIView

class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # If the request body is empty, provide a user-friendly message with required fields
        if not request.data:
            return Response({
                "detail": "You need to provide the following fields: 'items': [{'product': product_id, 'quantity': number_of_items}].",
                "example": {
                    "items": [
                        {"product": 1, "quantity": 2}
                    ]
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        items = request.data.get('items')

        if not items:
            return Response({"error": "No items provided in the order."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create order within a transaction to handle stock updates safely
            with transaction.atomic():
                order = Order.objects.create(user=request.user)

                # Process each item in the order
                for item in items:
                    product_id = item.get('product')
                    quantity = item.get('quantity')

                    if not product_id or not quantity:
                        return Response({
                            "error": "Each item must include 'product' and 'quantity'."
                        }, status=status.HTTP_400_BAD_REQUEST)

                    try:
                        product = Product.objects.get(id=product_id)
                    except Product.DoesNotExist:
                        return Response({"error": f"Product with id {product_id} not found."}, status=status.HTTP_404_NOT_FOUND)

                    if product.stock_quantity < quantity:
                        return Response({
                            "error": f"Insufficient stock for product {product.name}. Available stock: {product.stock_quantity}."
                        }, status=status.HTTP_400_BAD_REQUEST)

                    # Automatically set price_at_order based on the current product price
                    price_at_order = product.price

                    # Create OrderItem for each product and save the price at the time of order
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price_at_order=price_at_order
                    )

                    # Reduce stock quantity
                    product.stock_quantity -= quantity
                    product.save()

                return Response({"message": "Order created successfully!", "order_id": order.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        orders = Order.objects.filter(user=user)
        data = []

        for order in orders:
            order_items = order.items.all()
            items_data = []
            total_price = 0

            # Loop through each order item to calculate total price and format the response
            for item in order_items:
                item_total_price = item.price_at_order * item.quantity  # Calculate total price for the item
                total_price += item_total_price  # Add to order total

                # Add product name and other details to the items_data list
                items_data.append({
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "total_price": item_total_price
                })

            # Add the total price to the order response and include items data
            data.append({
                "order_id": order.id,
                "status": order.status,
                "created_at": order.created_at,
                "updated_at": order.updated_at,
                "total_price": total_price,
                "items": items_data
            })

        return Response(data, status=status.HTTP_200_OK)



class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id, *args, **kwargs):
        user = request.user
        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        order_items = order.items.all()
        items_data = [{
            "product_name": item.product.name,
            "quantity": item.quantity,
            "total_price": item.total_price()
        } for item in order_items]

        data = {
            "order_id": order.id,
            "status": order.status,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "total_price": order.total_price(),
            "items": items_data
        }

        return Response(data, status=status.HTTP_200_OK)