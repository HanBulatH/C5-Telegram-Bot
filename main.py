import json
import requests
import telebot
from configuration import TOKEN, API_KEY, valuts
from extensions import APIException, Convertor

# TOKEN = '2103356823:AAFlEl_IEpaWsXaaGYIZgsF7DhY3rHIVP7E'
# API_KEY = '0838cfc3e60e3b83ee4da0dfbed34667'

bot = telebot.TeleBot(TOKEN)

valuts = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'
}

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Начало работы!\nвведите команду в следующем формате:\n<имя валюты> \
\n<в какую валюту перевести> \
\n<кличество переводимой валюты>\n\nВывод списка валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Список валют:'
    for key in valuts.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Количество параметров введено неверно')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка в команде:\n{e}')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)




# @bot.message_handler(content_types=['text'])
# def convert(message: telebot.types.Message):
#     base, sym, amount = message.text.split(' ')
#     r = requests.get(f"https://api.exchangeratesapi.io/latest?access_key={API_KEY}&base={valuts[base]}&symbols={valuts[sym]}")
#     print(r.content)
#
#     # resp = json.loads(r.content)
#     # new_price = resp['rates'][sym_key] * amount
#     # new_price = round(new_price, 3)
#     # message = f"Цена {amount} {base} в {sym} : {new_price}"
#
#     total_base = json.loads(r.content)
#     result = total_base['rates'][sym] * amount
#     message = f'Цена {amount} {base} в {sym} - {result}'
#     bot.send_message(message.chat.id,  message)



bot.polling()