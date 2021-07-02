from django.urls import path

from app_cart import views

app_name = 'stroe'
urlpatterns = [
    path('detail/<slug:coupon>/', views.RetrieveCartView.as_view()),
    path('add/', views.AddToCartView.as_view()),
    path('clear/', views.ClearCartView.as_view()),
    path('delete/<int:product_id>/', views.DeleteCartItemView.as_view()),
]
