from django.db import models
from django.conf import settings
from products.models import Product  # Assuming you have a Product model in the products app

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='completed')  # pending, completed, canceled

    def __str__(self):
        return f"Order {self.id} by {self.user}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def reduce_stock(self):
        for item in self.items.all():
            item.product.reduce_stock_quantity(item.quantity)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.price_at_order * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
