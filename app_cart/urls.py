from django.urls import path

from app_cart import views

app_name = 'stroes'
urlpatterns = [
    path('detail/<slug:coupon>/', views.RetrieveCartView.as_view(), name='cart_detail_with_coupon'),
    path('detail/', views.RetrieveCartView.as_view(), name='cart_detail'),
    path('add/', views.AddToCartView.as_view(), name='add_cart_item'),
    path('clear/', views.ClearCartView.as_view(), name='delete_cart'),
    path('delete/<int:product_id>/', views.DeleteCartItemView.as_view(), name='delete_cart_item'),
]
