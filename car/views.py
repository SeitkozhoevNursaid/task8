import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.http import JsonResponse

from car.tasks import parse_car_page
from car.serializers import CarSerializer, CarCreateSerializer, CarUpdateSerializer, CarImgSerializer, CarParsingSerializer
from car.models import Car, CarImg, Category
from car.telegram import start_polling

class CarCreateAPIView(APIView):
    serializer_class = CarCreateSerializer

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


class CarImgRetrieveDestroyUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarImg.objects.all()
    serializer_class = CarImgSerializer


class CarImgListAPIView(generics.ListAPIView):
    queryset = CarImg.objects.all()
    serializer_class = CarImgSerializer


class CarParsingAPIView(APIView):
    def get(self, request, name):
        url = f"https://m.mashina.kg/new/search/{name}"
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')

            list_div = soup.find_all('div', class_='listing-item main')
            cars_data = []

            for div in list_div:
                links = div.find_all('a')
                for link in links:
                    car_url = f"https://m.mashina.kg{link['href']}"
                    car_data = parse_car_page.delay(car_url)
                    result = car_data.get()
                    cars_data.append(result)

            return JsonResponse(cars_data, safe=False)
        except Exception as e:
            return JsonResponse({'Ошибка': str(e)}, status=500)


class TestParsing(APIView):

    def get(self, request):
        url = 'https://m.mashina.kg/new/details/kia-k5-63ca2c96a9779355251584'
        page = requests.get(url)
        print(f"status{page}")
        soup = BeautifulSoup(page.text, 'html.parser')
        
        #обращение напрямую
        images = soup.find('div', class_='fotorama__img').find('img')
        
        #Дивы в диве
        div_page = soup.find("div", class_="page-content")
        up = div_page.find('div', class_='details-section ad')
        up1 = up.find('div', class_='left')
        up2 = up1.find('div', class_='content image')
        general = up2.find('div', class_='fotorama').find('img')
        
        if general:
            image = general.get('src')
        else:
            image = 'Без названия.jpeg'
        print(f"general:{image}")
        
        if images:
            list_images = list(images.get('src'))
        else:
            list_images = 'error'
        print(f"images:{list_images}")


class StartPolling(APIView):

    def get(self, request):
        start_polling()

        return Response('Бот запущен!')