from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
    quantity = serializers.IntegerField(min_value=1, required=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        if not items_data:
            raise serializers.ValidationError({"items": "You must provide at least one product and its quantity."})
        
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            product.reduce_stock_quantity(quantity)

        return order

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError({
                "items": "No items provided. Please include at least one product with a quantity in the format: 'items': [{'product': 1, 'quantity': 2}]"
            })
        return value
