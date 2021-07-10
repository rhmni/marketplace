from django.urls import path

from app_comment import views

app_name = 'comments'
urlpatterns = [
    path('', views.CommentListView.as_view(), name='list_of_comment'),
    path('add/', views.CreateCommentView.as_view(), name='create_comment'),
]
