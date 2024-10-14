from django.contrib import admin
from .models import Product, Category, Review, ProductImage, Wishlist, Discount


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Allows admins to add multiple images at once


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1  # Allows admins to add reviews directly within the product's admin page



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'created_date', 'updated')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'price', 'stock_quantity', 'created_date')
    inlines = [ProductImageInline, ReviewInline]  # Show related images and reviews in product admin
    date_hierarchy = 'created_date'
    readonly_fields = ('created_date', 'updated')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username')
    list_filter = ('rating', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_url')
    search_fields = ('product__name',)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('products',)  # This allows admins to select products in a ManyToMany relationship


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percentage', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('product__name',)
