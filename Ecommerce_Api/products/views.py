from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .models import Product, Category, Review, ProductImage,Discount, Wishlist
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer, ProductImageSerializer, DiscountSerializer, WishlistSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

# ViewSet for handling CRUD operations for Products
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('created_date')  # Order by created_date
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'category__name']  # Enable searching by name and category name
    ordering_fields = ['price', 'name', 'stock_quantity']
    permission_classes = [IsAuthenticated]  # Only authenticated users can manage products

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        # Get the 'category' query parameter
        category_name = self.request.query_params.get('category', None)
        search_query = self.request.query_params.get('search', None)

        # Handle category filtering and raise error if no results are found
        if category_name and not queryset.exists():
            raise ValidationError(
                detail={"error": f"There is no category like '{category_name}'"},
                code=status.HTTP_404_NOT_FOUND
            )

        # Handle search query and raise error if no results are found
        if search_query and not queryset.exists():
            raise ValidationError(
                detail={"error": f"No products found matching the search term '{search_query}'"},
                code=status.HTTP_404_NOT_FOUND
            )

        return queryset


# ViewSet for handling CRUD operations for Categories
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Authenticated users can create/update/delete, others can read
 
class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        image_urls = request.data.get('image_urls')

        if not product_id or not image_urls or not isinstance(image_urls, list):
            return Response(
                {
                    "error": {
                        "message": "Both 'product_id' and 'image_urls' (as an array) are required.",
                        "product_id": product_id,
                        "image_urls": image_urls
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create ProductImage instances for each image URL
        product_images = []
        for image_url in image_urls:
            product_image = ProductImage(product=product, image_url=image_url)
            product_image.save()
            product_images.append(product_image)

        serializer = ProductImageSerializer(product_images, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # Allows partial updates
        instance = self.get_object()  # Get the image instance to be updated
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()  # Save the updated image
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Get the image instance to be deleted
        instance.delete()  # Delete the image
        return Response({"message": "Image deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class DiscountCreateView(generics.CreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]

class DiscountUpdateView(generics.UpdateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]

class DiscountDeleteView(generics.DestroyAPIView):
    queryset = Discount.objects.all()
    permission_classes = [IsAuthenticated]

class DiscountListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    

class AddToWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({"error": "Product ID is required."}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)

        # Get or create the user's wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)

        if product in wishlist.products.all():
            return Response({"message": "Product already in wishlist."}, status=200)

        wishlist.products.add(product)  # Add product to wishlist
        wishlist.save()

        return Response({"message": "Product added to wishlist."}, status=201)
    
class WishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            products = wishlist.products.all()
            product_data = [{
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "description": product.description
            } for product in products]
            return Response({"wishlist": product_data}, status=status.HTTP_200_OK)
        except Wishlist.DoesNotExist:
            return Response({"wishlist": []}, status=status.HTTP_200_OK)  # Return an empty wishlist
    

class WishlistUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Expecting a JSON body with product_id
        product_id = request.data.get('product_id')
        action = request.data.get('action')  # 'add' or 'remove'

        if not product_id or not action:
            return Response({"error": "product_id and action ('add' or 'remove') are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        wishlist, created = Wishlist.objects.get_or_create(user=request.user)

        if action == 'add':
            wishlist.products.add(product)
            return Response({"message": "Product added to wishlist."}, status=status.HTTP_200_OK)
        elif action == 'remove':
            wishlist.products.remove(product)
            return Response({"message": "Product removed from wishlist."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid action. Use 'add' or 'remove'."}, status=status.HTTP_400_BAD_REQUEST)




# Submit a Review (Create)
class SubmitReviewAPIView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product = Product.objects.get(pk=self.kwargs['product_id'])  # Get product from URL
        serializer.save(user=self.request.user, product=product)  # Attach user and product to the review

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Review created successfully!"}, status=status.HTTP_201_CREATED)

# Retrieve Reviews for a Product (List)
class ProductReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product__id=product_id)

# Update a Review
class ReviewUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user, product__id=self.kwargs['product_id'])

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Review updated successfully!"}, status=status.HTTP_200_OK)

# Delete a Review
class ReviewDeleteAPIView(generics.DestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user, product__id=self.kwargs['product_id'])

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Review deleted successfully!"}, status=status.HTTP_200_OK)