import requests
from bs4 import BeautifulSoup
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.http import JsonResponse
from celery import shared_task

from car.tasks import run_telegram_bot
from car.serializers import CarSerializer, CarCreateSerializer, CarUpdateSerializer, CarImgSerializer, CarParsingSerializer
from car.models import Car, CarImg, Category


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


class RunTelegramBot(APIView):

    def get(self, request):
        run_telegram_bot.delay()

        return Response('Бот успешно запущен!')


class CarParsingAPIView(APIView):
    def get(self, request, name):
        url = f"https://m.mashina.kg/new/search/{name}"
        print(f"requestttttt{url}")
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')

            list_div = soup.find_all('div', class_='listing-item main')
            cars_data = []

            for div in list_div:
                links = div.find_all('a')
                for link in links:
                    car_url = f"https://m.mashina.kg{link['href']}"
                    print(f"Ссылка машины: {car_url}")
                    car_data = self.parse_car_page(car_url)
                    cars_data.append(car_data)

            return JsonResponse(cars_data, safe=False)
        except Exception as e:
            return JsonResponse({'Ошибка': str(e)}, status=500)

    def parse_car_page(self, url):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            description_element = soup.find('div', class_='characteristics')

            """Категория"""
            for category_element in description_element:
                category_element = description_element.find_all('div', class_='info')

                categoryslice = category_element[1]
                category_value = categoryslice.find('span', class_='value')

                if category_element:
                    category = category_value.get_text(strip=True)
                else:
                    category = 'Нет категории'

            """Описание"""
            if description_element:
                description = description_element.get_text(strip=True)
            else:
                description = 'Нет описания'

            """Картинка"""
            div_page = soup.find("div", class_="page-content")
            up = div_page.find('div', class_='details-section ad')
            up1 = up.find('div', class_='left')
            up2 = up1.find('div', class_='content image')
            general = up2.find('div', class_='fotorama').find('img')

            if general:
                image = general.get('src')
            else:
                image = 'Без названия.jpeg'

            """Название"""
            div_page = soup.find("div", class_="page-content")
            for name_element in div_page:
                name_element = div_page.find('h1')
                if name_element:
                    name = name_element.get_text(strip=True)
                else:
                    name = 'Нет названия'

            """Цена"""
            price_element = soup.find("span", class_="white custom-margins font-big")
            if price_element:
                price = price_element.get_text(strip=True)
            else:
                price = 'Нет цены'

            category, new_category = Category.objects.get_or_create(name=category)
            car, created = Car.objects.get_or_create(name=name, price=price, defaults={'description': description, 'category': category})
            car_img = CarImg.objects.get_or_create(name=car, images=image)

            if created:
                print(f"Создана новая машина: {name}")
            else:
                print(f"Машина: {name}")

            if new_category:
                print("Создано")
            else:
                print('Отлично')

            return {'name': name, 'price': price, 'description': description, 'image': image}

        except Exception as e:
            print(f"Ошибка при парсинге страницы машины {url}: {str(e)}")
            return {'Ошибка': str(e)}
