import telebot
import webbrowser
import sqlite3
from telebot import types
bot = telebot.TeleBot(token='5937676517:AAEG8U11wayyFFQmbJKi3Y3BdINCzUTIDWs')


@bot.message_handler(commands=['start', 'main', 'hello'])
def main(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Перейти на сайт"))
    markup.add(types.KeyboardButton("Удалить фото"))
    markup.add(types.KeyboardButton("Изменить текст"))
    file = open("house.jpg", "rb")
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    #bot.send_message(message.chat.id, "Hello", reply_markup=markup)
    #bot.send_audio(message.chat.id, "Hello", reply_markup=markup)
    #bot.send_video(message.chat.id, "Hello", reply_markup=markup)
    #bot.send_message(message.chat.id, "Hello", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == "Перейти на сайт":
        bot.send_message(message.chat.id, "Website is open")
    elif message.text == "Удалить фото":
        bot.send_message(message.chat.id, "Website is closed")
@bot.message_handler(content_types=['photo'])
def get_photos(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перейти на сайт", url='https://www.instagram.com/mischa.makaronn'))
    markup.add(types.InlineKeyboardButton("Удалить фото", callback_data='delete'))
    markup.add(types.InlineKeyboardButton("Изменить текст", callback_data='edit'))

    bot.reply_to(message, "Классная фотка", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "delete":
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == "edit":
        bot.edit_message_text('edit text', callback.message.chat.id, callback.message.message_id)

@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://www.instagram.com/mischa.makaronn')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '<b>help</b> <u>information</u>', parse_mode='html')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет  {message.from_user.first_name}, {message.from_user.username}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')
    elif message.text.lower() == '/start':
        bot.send_message(message.chat.id, f'Привет  {message.from_user.first_name}')



bot.polling(none_stop=False)



