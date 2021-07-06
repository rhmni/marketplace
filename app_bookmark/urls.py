from django.urls import path

from app_bookmark import views

app_name = 'bookmark'
urlpatterns = [
    path('add/', views.CreateBookmarkView.as_view(), name='add_bookmark'),
]
