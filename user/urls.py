from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('auth/', TokenObtainPairView.as_view()),
    path('auth/refresh', TokenRefreshView.as_view()),
]
