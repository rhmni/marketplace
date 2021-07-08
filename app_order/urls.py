from django.urls import path

from app_order import views

app_name = 'orders'

urlpatterns = [
    path('checkout/<slug:coupon>/', views.OrderCheckoutView.as_view(), name='checkout_cart_with_coupon'),
    path('checkout/', views.OrderCheckoutView.as_view(), name='checkout_cart'),
]
