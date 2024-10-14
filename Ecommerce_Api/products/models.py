from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.utils import timezone
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=255, unique = True)
    description = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return self.name 


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0.01))])
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='categories') # ForeignKey to Category
    stock_quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    image_url = models.URLField()
    created_date = models.DateTimeField(auto_now_add=True)   
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null= False, blank=False)
    updated = models.DateTimeField(auto_now=True)

    def reduce_stock_quantity(self, quantity):
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save()
        else:
            raise ValueError("Not enough stock available")

    def __str__(self):
        return self.name
    
    def get_discounted_price(self):
        active_discount = self.discounts.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()).first()
        if active_discount:
            discount_amount = self.price * (active_discount.discount_percentage / 100)
            return self.price - discount_amount
        return self.price

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} - {self.user.email}' 

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlisted_by')
   

    # class Meta:
    #     unique_together = ('user', 'product')  # Prevents duplicate entries of the same product in a user's wishlist

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"
    
class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


    def __str__(self):
        return f"{self.discount_percentage}% off on {self.product.name}"

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date