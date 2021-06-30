from django.urls import path

from app_store import views

app_name = 'store'

urlpatterns = [
    path('', views.RetrieveStoreView.as_view(), name='retrieve_store'),
    path('create/', views.CreateStoreView.as_view(), name='create_store'),
    path('update/', views.UpdateStoreView.as_view(), name='update_store'),
]
