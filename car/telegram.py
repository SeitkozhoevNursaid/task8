import telebot
import requests

from decouple import config


TOKEN = config('TOKEN')
bot = telebot.TeleBot(TOKEN)

def polling_thread():
    bot.polling(none_stop=True)


@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_welcome = telebot.types.InlineKeyboardButton(
        text='Начнем Родные?'
    )
    keyboard.add(button_welcome)
    bot.send_message(chat_id,
                     'Добро пожаловать Родниковый Период в парсинг бота сайта "Mashina.kg"',
                     reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Начнем Родные?')
def choose_car(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Kia', 'Hyundai', 'Geely', 'Toyota']
    keyboard.add(*[telebot.types.InlineKeyboardButton(text=car) for car in buttons])
    bot.send_message(chat_id, 'Выберите марку машины для просмотра актуальных машин', reply_markup=keyboard)


@bot.message_handler(content_types='text')
def reply_message(message):
    chat_id = message.chat.id
    text = message.text

    if text in ['Kia', 'Hyundai', 'Geely', 'Toyota']:
        image = 'https://placekitten.com/200/200'
        bot.send_photo(chat_id, image)
        bot.send_message(chat_id, 'Подождите 5 секунд, идет поиск...')
        data = get_car_data(text)
        send_car_data(chat_id, data)
    else:
        bot.send_message(chat_id, 'Выберите марку машин из кнопок')


def get_car_data(text:str):
    try:
        name = text.lower()
        url = f'http://127.0.0.1:8000/api/car/parsing/{name}/'
        response = requests.get(url=url)
        if response.status_code == 200:
            data = response.json()
            print(f"data:::::{data}")
            return data
        else:
            return {'Ошибка': 'Ошибка при получении данных машины'}
    except Exception as e:
        print(f"Ошибка при получении данных машины: {str(e)}")
        return {'Ошибка': str(e)}


def send_car_data(chat_id, data):
    for i in data:
        if 'Ошибка' in i:
            bot.send_message(chat_id, f"Ошибка: {i['Ошибка']}")
        else:
            name = i.get('name', 'Нет данных о названии')
            price = i.get('price', 'Нет данных о цене')
            description = i.get('description', 'Нет описания')
            image = i.get('image', 'https://placekitten.com/200/200')

            description_lines = description
            formatted_string = description_lines.replace('Характеристики', '\nХарактеристики').replace('Год выпуска', '\nГод выпуска ').replace('Кузов', '\nКузов ').replace('Цвет', '\nЦвет ').replace('Двигатель', '\nДвигатель ').replace('Коробка передач', '\nКоробка передач ').replace('Привод', '\nПривод ').replace('Расход топлива,', '\nРасход топлива ').replace('Разгон до 100 км/ч,', '\nРазгон до 100 км/ч, ')
            
            message = f"Название: {name}\nЦена: {price}\nОписание:{formatted_string}"
            bot.send_photo(chat_id, image)
            bot.send_message(chat_id, message)
