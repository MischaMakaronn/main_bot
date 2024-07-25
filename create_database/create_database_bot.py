import sqlite3

import telebot
import sqlite3
from telebot import types
bot = telebot.TeleBot(token='5937676517:AAEG8U11wayyFFQmbJKi3Y3BdINCzUTIDWs')

name = None
@bot.message_handler(commands = ['start'])
def start(message):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    password TEXT
                )''')

    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, "Hello, I'll register you now. Enter your name ")
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password))
    conn.commit()
    cur.close()
    conn.close()
    markup = types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup = markup)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT *FROM users ')
    users = cur.fetchall()
    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)







bot.polling(none_stop=True)