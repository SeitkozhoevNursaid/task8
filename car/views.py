import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from car.tasks import parse_car_page
from car.serializers import CarSerializer, CarCreateSerializer, CarUpdateSerializer, CarImgSerializer
from car.models import Car, CarImg


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


class CarUpdateAPIView(APIView):  # TODO: APIVIEW or Generics
    serializer_class = CarUpdateSerializer

    def patch(self, request, pk):  # TODO: Validation pk
        object = get_object_or_404(pk=pk)
        serializer = self.serializer_class(object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Успешно!', status=200)


class CarRetrieveAPIView(APIView):
    serializer_class = CarSerializer

    def get(self, request, pk):  # TODO: validation pk
        object = get_object_or_404(pk=pk)
        serializer = self.serializer_class(object)

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
            soup = BeautifulSoup(page.text, 'lxml')

            list_div = soup.find_all('div', class_='listing-item main')
            cars_data = []

            for div in list_div:
                links = div.find_all('a')
                for link in links:
                    car_url = f"https://m.mashina.kg{link['href']}"
                    car_data = parse_car_page.delay(car_url)  # TODO: Celery смысл?
                    result = car_data.get()
                    cars_data.append(result)

            return JsonResponse(cars_data, safe=False)  # TODO: safe
        except Exception as e:
            return JsonResponse({'Ошибка': str(e)}, status=500)


class TestParsing(APIView):

    def get(self, request):
        url = 'https://m.mashina.kg/new/details/kia-k5-63ca2c96a9779355251584'
        
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')  # lxml look at it
        
        container = soup.find('div', class_='characteristics')
        print(container.text.strip())
        # description_element = container.find_all('div', class_='info')
        # for i in description_element:
        #     print(i.text.strip())

        # """Категория"""
        # category_element = [container.find_all('div', class_='info') for i in container][1]
        # for category_value in category_element:
        #     category_value = category_element.find('span', class_='value')
        # print(category_value)
            # category_value = categoryslice.find('span', class_='value')
            # if category_element:
            #     category = category_value.get_text(strip=True)
            # else:
            #     category = 'Нет категории'

        # """Описание"""
        # if description_element:
        #     description = description_element.get_text(strip=True)
        # else:
        #     description = 'Нет описания'

        # """Картинка"""
        # div_page = soup.find("div", class_="page-content")
        # up = div_page.find('div', class_='details-section ad')
        # up1 = up.find('div', class_='left')
        # up2 = up1.find('div', class_='content image')
        # general = up2.find('div', class_='fotorama').find('img')
        # if general:
        #     image = general.get('src')
        # else:
        #     image = 'Без названия.jpeg'

        # """Название"""
        # div_page = soup.find("div", class_="page-content")
        # for name_element in div_page:
        #     name_element = div_page.find('h1')
        #     if name_element:
        #         name = name_element.get_text(strip=True)
        #     else:
        #         name = 'Нет названия'

        # """Цена"""
        # price_element = soup.find("span", class_="white custom-margins font-big")
        # if price_element:
        #     price = price_element.get_text(strip=True)
        # else:
        #     price = 'Нет цены'
        # category, new_category = Category.objects.get_or_create(name=category)
        # car, created = Car.objects.get_or_create(name=name, price=price, defaults={'description': description, 'category': category})
        # CarImg.objects.get_or_create(name=car, images=image)

        # data = {'name': name, 'price': price, 'description': description, 'image': image}
        # return data

        return Response('asda')