from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, SubmitReviewAPIView, ProductReviewListAPIView,ReviewUpdateAPIView,ReviewDeleteAPIView, ProductImageViewSet, DiscountCreateView, DiscountUpdateView, DiscountDeleteView, AddToWishlistView, WishlistAPIView, WishlistUpdateAPIView,DiscountListAPIView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'product-images', ProductImageViewSet, basename='product-images'),
router.register(r'', ProductViewSet, basename='product')

# router.register(r'discounts', DiscountViewSet, basename='discount')


urlpatterns = [
    path('wishlist/', WishlistAPIView.as_view(), name='wishlist'),  # Get wishlist
    path('discounts/create/', DiscountCreateView.as_view(), name='create-discount'),
    path('discounts/update/<int:pk>/', DiscountUpdateView.as_view(), name='update-discount'),
    path('discounts/delete/<int:pk>/', DiscountDeleteView.as_view(), name='delete-discount'),
    path('discounts/', DiscountListAPIView.as_view(), name='discount-list'),
    path('wishlist/add/', AddToWishlistView.as_view(), name='wishlist-add'),
    path('wishlist/update/', WishlistUpdateAPIView.as_view(), name='wishlist-update'),  # Add/Remove product
    path('<int:product_id>/reviews/', ProductReviewListAPIView.as_view(), name='product-reviews-list'),
    path('<int:product_id>/reviews/add/', SubmitReviewAPIView.as_view(), name='submit-review'),
    path('<int:product_id>/reviews/<int:pk>/update/', ReviewUpdateAPIView.as_view(), name='update-review'),
    path('<int:product_id>/reviews/<int:pk>/delete/', ReviewDeleteAPIView.as_view(), name='delete-review'),
 
    path('', include(router.urls)),
]
urlpatterns += router.urls

