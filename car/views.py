from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from car.serializers import CarSerializer, CategorySerializer, CarUpdateSerializer
from car.models import Car


class CarCreateAPIView(APIView):
    serializer_class = CarSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Успешно!', status=201)


class CarListAPIView(APIView):
    serializer_class = CarSerializer

    def get(self, request):
        queryset = Car.objects.all()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)


class CarDestroyAPIView(generics.DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response('Вы удалили обьект!', status=200) 


class CarUpdateAPIView(APIView):
    serializer_class = CarUpdateSerializer

    def patch(self, request, pk):
        queryset = Car.objects.get(pk=pk)
        serializer = self.serializer_class(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Успешно!', status=200)


class CarRetrieveAPIView(APIView):
    serializer_class = CarSerializer

    def get(self, request, pk):
        queryset = Car.objects.get(pk=pk)
        serializer = self.serializer_class(queryset)

        return Response(serializer.data)