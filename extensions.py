"""
Здесь описана основная логика и использование API
"""


import requests
import json

from config import keys, headers


# Класс собственного исключения
# нужен для разделения ошибок на пользовательские и системные
class APIException(Exception):
    pass


# Класс для конвертирования
class Converter:
    # статические метод для получения результата конвертации
    @staticmethod
    # принимаем три параметра (что конвертируем, во что конвертируем и сколько)
    def get_price(quote: str, base: str, amount: str):

        try:
            # если количество задано верно, записываем его в переменную
            amount = float(amount)
        # а если нет, выкидываем исключение
        except ValueError:
            raise APIException(f"Не верно задано количество - {amount}")

        # если валюта одна и таже
        if quote == base:
            # тоже выкидываем исключение
            raise APIException(f"Нужно вводить разные валюты")

        try:
            # если неверно зада валюта
            quote_ticket = keys[quote]
        #     выкидываем исключение
        except KeyError:
            raise APIException(f"Не верно задана валюта {quote}")

        try:
            # если неверно зада валюта
            base_ticket = keys[base]
            # выкидываем исключение
        except KeyError:
            raise APIException(f"Не верно задана валюта {quote}")

        # формирование ссылки для дальнейшего запроса
        url = f"https://api.apilayer.com/fixer/convert?to={base_ticket}&from={quote_ticket}&amount={amount}"
        # отправляем запрос
        r = requests.get(url, headers)
        # извлекаем результат из json объекта, который содержит результат нашего запроса
        total = json.loads(r.content)['result']
        # возвращаем округленный результат
        return round(total, 2)