import requests
from bs4 import BeautifulSoup
from celery import shared_task

from car.models import Car, Category, CarImg


@shared_task
def parse_car_page(url):
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

        data = {'name': name, 'price': price, 'description': description, 'image': image}
        return data

    except Exception as e:
        print(f"Ошибка при парсинге страницы машины {url}: {str(e)}")
        return {'Ошибка': str(e)}
