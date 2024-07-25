import telebot
import requests
import json

bot = telebot.TeleBot(token='5937676517:AAEG8U11wayyFFQmbJKi3Y3BdINCzUTIDWs')
API = '2426a738848bd26aad79b8c8b92c62a8'
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, рад тебя видеть! Напиши название города погоду которого хочешь узнать!')



@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Сейчас погода: {temp} °C')

        image = 'sun.png' if temp > 10.0 else 'tuchi.png'

        file = open('./' + image, 'rb')

        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, 'Город указан не верно')

bot.polling(none_stop=True)