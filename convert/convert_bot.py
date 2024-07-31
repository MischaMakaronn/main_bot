from currency_converter import CurrencyConverter
# Date,USD,JPY,BGN,CYP,CZK,DKK,EEK,GBP,HUF,LTL,LVL,MTL,PLN,ROL,RON,SEK,SIT,SKK,CHF,ISK,NOK,HRK,RUB,
# TRL,TRY,AUD,BRL,CAD,CNY,HKD,IDR,ILS,INR,KRW,MXN,MYR,NZD,PHP,SGD,THB,ZAR,
import telebot
from telebot import types
bot = telebot.TeleBot(token='5937676517:AAEG8U11wayyFFQmbJKi3Y3BdINCzUTIDWs')

currency = CurrencyConverter()
amount = 0
@bot.message_handler(commands = ["start"])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())

    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат, впишите сумму цифрами')
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width = 2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data = 'usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data = 'eur/usd')
        btn3 = types.InlineKeyboardButton('USD/PLN', callback_data = 'usd/pln')
        btn4 = types.InlineKeyboardButton('PLN/USD', callback_data = 'pln/usd')
        btn5 = types.InlineKeyboardButton('USD/CAD', callback_data = 'usd/cad')
        btn6 = types.InlineKeyboardButton('Другое значение', callback_data = 'else')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число быть больше нуля, впишите сумму')
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново ввести сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через "/"')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново ввести сумму')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так. Впишите значение заново типа "USD/EUR"')
        bot.register_next_step_handler(message, my_currency)


bot.polling(none_stop = True)