"""
В этом файле реализован сам бот и его обработчики
"""


import telebot  # библиотека для создания ботов

from config import TOKEN, keys  # берем токен и список валют из файла
from extensions import Converter, APIException  # берем наши исключения и классы
from markup import create_markup  # импортируем клавиатуру для телеграма


bot = telebot.TeleBot(TOKEN)  # создаем бота


# Обработчик команд старт и хелп
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):  # берем в обработку сообщение
    # формируем текст, который бот будет отправлять в ответ на команды
    text = """Чтобы конвертировать валюту, вам нужно ввести данные в формате:
<валюта> <во что конвертировать> <количество>
Чтобы получить список валют, введите: /values"""
    bot.reply_to(message, text)  # отправляем наш текст в ответ на сообщение


# обработчик команды значения, который выводит список валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):  # принимаем сообщение с командой
    # формируем текст ответа
    text = "Доступные валюты:"
    # пробегаемся по всем ключам в списке(словаре)
    for key in keys:
        # добавляем к тексту, с новой строки, каждый ключ
        text = '\n'.join((text, key))
    bot.reply_to(message, text)  # отправляем текст в ответ на команду


# *** Второй вариант (похож на диалог) ***
# обработчик, который обработает команду на конвертацию
@bot.message_handler(commands=['convert'])
def convert(message: telebot.types.Message):  # принимаем сообщение с командой
    # формируем текст ответа
    text = "Выберите валюту из которой хотите конвертировать"
    bot.send_message(message.chat.id, text, reply_markup=create_markup())  # отправляем текст в ответ на команду
    bot.register_next_step_handler(message, quote_handler)  # регистрируем следующий обработчик


# обработчик получения первой валюты
def quote_handler(message: telebot.types.Message):
    quote = message.text.strip().lower()  # запоминаем валюту
    text = "Выберите валюту в которую хотите конвертировать"  # создаем ответ
    bot.send_message(message.chat.id, text, reply_markup=create_markup(quote))  # отправляем ответ
    bot.register_next_step_handler(message, base_handler, quote)  # регистрируем следующий обработчик
                                                                  # и передаем в него валюту


# обработчик получения второй валюты, принимаем и храним первую
def base_handler(message: telebot.types.Message, quote):
    base = message.text.strip().lower()  # получаем вторую валюту
    text = "Выберите количество которое хотите конвертировать"  # формируем ответ
    bot.send_message(message.chat.id, text) # отправляем ответ
    bot.register_next_step_handler(message, amount_handler, quote, base)  # регистрируем следующий обработчик
                                                                          # и передаем в него обе валюты


# обработчик количества, принимаем обе валюты
def amount_handler(message: telebot.types.Message, quote, base):
    amount = message.text.strip()  # получаем количество
    try:
        total_base = Converter.get_price(quote, base, amount)  # выполняем конвертацию
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации \n{e}")
    else:
        text = f"{amount} {quote} - это {total_base} {base}"  # формируем ответ
        bot.send_message(message.chat.id, text)  # отправляем ответ

# *** Первый вариант (грубый) ***
# # обработчик сообщения с данными для конвертации валюты
# @bot.message_handler(content_types=['text'])  # определяем тип
# def convert(message: telebot.types.Message):  # принимаем сообщение
#     # отлавливая исключения
#     try:
#         # разбиваем полученный текст на три части
#         values = message.text.split()
#
#         # если передано не три параметра
#         if len(values) != 3:
#             # поднимаем наше исключение с текстом
#             raise APIException("Необходимо  вводить 3 значения.")
#
#         # а если с параметрами все ок, записываем каждый параметр в свою переменную
#         quote, base, amount = values
#         # передаем наши параметры в метод класса и получаем результат конвертации
#         total_base = Converter.get_price(quote, base, amount)
#     # если поймали наше исключение
#     except APIException as e:
#         # выводим сообщение об ошибки в чат
#         bot.reply_to(message, f"Ошибка пользователя\n{e}")
#     # если поймали исключение
#     except Exception as e:
#         # так же выводим сообщение
#         bot.reply_to(message, f"Не удалось выполнить команду\n{e}")
#     # а если все хорошо
#     else:
#         # формируем текст ответа
#         text = f"{amount} {quote} - это {total_base} {base}"
#         # отвечаем в чате
#         bot.send_message(message.chat.id, text)


# запуск бота
bot.polling(none_stop=True)