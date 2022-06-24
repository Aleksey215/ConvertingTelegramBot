"""
Файл для написания клавиатуры, с помощью которой можно общаться с ботом
"""

from telebot import types
from config import keys


# создание динамической клавиатуры
def create_markup(base=None):
    # объявляем клавиатуру, которая будет выводиться только в момент вызова обработчика
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    # список кнопок
    buttons = []
    # для всех ключей из словаря валют
    for key in keys.keys():
        # если ключа нет в base
        if key != base:
            # добавляем кнопку с его именем в список
            buttons.append(types.KeyboardButton(key.capitalize()))
    # добавляем кнопки в клавиатуру
    markup.add(*buttons)
    # возвращаем клавиатуру
    return markup
