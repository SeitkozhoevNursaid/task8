from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.views import (
    RegistrationAPIView, VerifyEmail, ChangePassword,
    ForgotPassword,
    ConfirmForgotPassword,
    AdminResetPassword,
)


urlpatterns = [
    path('auth/', TokenObtainPairView.as_view()),
    path('auth/refresh', TokenRefreshView.as_view()),
    path('register/', RegistrationAPIView.as_view()),
    path('email-verify/<uuid:activation_code>/', VerifyEmail.as_view()),
    path('change_password/', ChangePassword.as_view()),
    path('forgot-password/', ForgotPassword.as_view()),
    path('confirm-forgot-password/<str:pk>/', ConfirmForgotPassword.as_view()),
    path('reset_password/', AdminResetPassword.as_view())
]
