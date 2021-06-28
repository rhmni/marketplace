from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from app_account import views

app_name = 'account'
urlpatterns = [
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User Register Verification
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('register/verify/', views.UserVerificationView.as_view(), name='user_register'),
]
