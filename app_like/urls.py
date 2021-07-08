from django.urls import path

from app_like import views

app_name = 'likes'
urlpatterns = [
    path('like/', views.LikeView.as_view(), name='like_product'),
    path('dislike/', views.DisLikeView.as_view(), name='dislike_product'),
]
