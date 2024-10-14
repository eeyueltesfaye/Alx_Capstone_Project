from django.urls import path
from .views import OrderCreateAPIView, OrderListAPIView, OrderDetailAPIView

urlpatterns = [
    path('create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('list/', OrderListAPIView.as_view(), name='order-list'),
    path('<int:order_id>/', OrderDetailAPIView.as_view(), name='order-detail'),

]
