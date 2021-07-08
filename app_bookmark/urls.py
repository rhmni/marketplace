from django.urls import path

from app_bookmark import views

app_name = 'bookmarks'
urlpatterns = [
    path('', views.ListBookmarkView.as_view(), name='show_bookmark'),
    path('add/', views.CreateBookmarkView.as_view(), name='add_bookmark'),
    path('delete/<product_id>/', views.DeleteBookmarkView.as_view(), name='delete_bookmark'),
]
