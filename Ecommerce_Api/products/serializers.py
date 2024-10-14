from rest_framework import serializers
from .models import Product, Category, Review, ProductImage, Wishlist, Discount 
from django.utils import timezone


# Serializer for Category to handle CRUD for categories
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductImageSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product')  # Allow setting product by id
    class Meta:
        model = ProductImage
        fields = ['id', 'product_id', 'image_url']

    def validate_image_url(self, value):
        if not value:
            raise serializers.ValidationError("Image URL cannot be empty.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField() 
    images = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field='name',  # This allows us to use the category's name instead of its ID
        queryset=Category.objects.all()  # Ensures that the category exists in the database
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'discounted_price', 'category', 
            'stock_quantity', 'image_url', 'created_date', 'created_by', 'updated', 'images'
        ]

    def validate_category(self, value):
        try:
            category = Category.objects.get(name__iexact=value)
            return category
        except Category.DoesNotExist:
            raise serializers.ValidationError(f"Category with name '{value}' does not exist.")

     # Method to return image URLs separated by commas
    def get_images(self, obj):
        images = obj.images.all()  # Assuming 'images' is the related_name for ProductImage model
        image_urls = [image.image_url for image in images]
        return ', '.join(image_urls)  # Return the URLs as a comma-separated string

    def update(self, instance, validated_data):
        # Handle the update of the product's fields
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.category = validated_data.get('category', instance.category)
        instance.stock_quantity = validated_data.get('stock_quantity', instance.stock_quantity)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        
        # Update images if necessary
        images_data = validated_data.get('images')
        if images_data:
            instance.images.all().delete()  # Delete old images
            for image_data in images_data:
                ProductImage.objects.create(product=instance, **image_data)

        instance.save()
        return instance

    def get_discounted_price(self, obj):
        # Retrieve the discount for the product, if it exists
        discount = Discount.objects.filter(product=obj).first()
        if discount:
            return {
                "discounted_price": obj.price - (obj.price * discount.discount_percentage / 100),
                "start_date": discount.start_date,
                "end_date": discount.end_date
            }
        return obj.price  # Return regular price if no discount
    
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display user as a string (email or username)
    product = serializers.StringRelatedField(read_only=True)  # Display product name instead of product ID

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'created_at']

    def create(self, validated_data):
        # Automatically assign the logged-in user and product to the review
        return Review.objects.create(**validated_data)
    def validate(self, data):
        user = self.context['request'].user
        product = self.context['view'].kwargs['product_id']
        if Review.objects.filter(user=user, product_id=product).exists():
            raise serializers.ValidationError("You have already submitted a review for this product.")
        return data

class DiscountSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)  # For product name
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),  # Make product_id required and ensure it exists
        source='product',  # It refers to the 'product' field in the Discount model
        required=True
    )
    class Meta:
        model = Discount
        fields = ['id', 'product_id','product_name', 'discount_percentage', 'start_date', 'end_date']

    def validate(self, data):
        # Ensure start_date is before end_date
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after the start date.")
        return data


class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'product_name']
        read_only_fields = ['user']
    
