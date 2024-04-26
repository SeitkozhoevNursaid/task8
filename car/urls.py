from django.urls import path

from car.views import (
    CarCreateAPIView,
    CarDestroyAPIView,
    CarListAPIView,
    CarRetrieveAPIView,
    CarUpdateAPIView)


urlpatterns = [
    path('cars/', CarListAPIView.as_view()),
    path('car/create/', CarCreateAPIView.as_view()),
    path('car/<int:pk>/', CarRetrieveAPIView.as_view()),
    path('car/delete/<int:pk>/', CarDestroyAPIView.as_view()),
    path('car/update/<int:pk>/', CarUpdateAPIView.as_view()),
]