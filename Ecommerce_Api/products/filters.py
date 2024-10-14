import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    stock_min = django_filters.NumberFilter(field_name='stock_quantity', lookup_expr='gte')
    stock_max = django_filters.NumberFilter(field_name='stock_quantity', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')  # Filter by category name (partial match)

    class Meta:
        model = Product
        fields = ['price_min', 'price_max', 'stock_min', 'stock_max', 'category']
