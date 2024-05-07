from django.urls import path

from car.views import (
    CarCreateAPIView,
    CarDestroyAPIView,
    CarListAPIView,
    CarRetrieveAPIView,
    CarUpdateAPIView,
    CarImgRetrieveDestroyUpdate,
    CarParsingAPIView,
    TestParsing,
    StartPolling,
    CarImgListAPIView)


urlpatterns = [
    path('cars/', CarListAPIView.as_view()),
    path('car/create/', CarCreateAPIView.as_view()),
    path('car/<int:pk>/', CarRetrieveAPIView.as_view()),
    path('car/delete/<int:pk>/', CarDestroyAPIView.as_view()),
    path('car/update/<int:pk>/', CarUpdateAPIView.as_view()),
    path('car/images/', CarImgListAPIView.as_view()),
    path('car/image/<int:pk>/', CarImgRetrieveDestroyUpdate.as_view()),
    path('car/parsing/<str:name>/', CarParsingAPIView.as_view()),
    path('test/', TestParsing.as_view()),
    path('start/', StartPolling.as_view())
]
