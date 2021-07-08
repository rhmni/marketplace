from django.urls import path

from app_store import views

app_name = 'stores'

urlpatterns = [
    path('', views.RetrieveStoreView.as_view(), name='retrieve_store'),
    path('create/', views.CreateStoreView.as_view(), name='create_store'),
    path('update/', views.UpdateStoreView.as_view(), name='update_store'),
    path('checkout/', views.StoreCheckoutView.as_view(), name='checkout_store'),
    path('checkouts/', views.RetrieveStoreCheckout.as_view(), name='checkout_store'),
]
