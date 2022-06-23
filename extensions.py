import requests
import json
from config import keys, headers


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не верно задано количество - {amount}")

        if quote == base:
            raise APIException(f"Нужно вводить разные валюты")

        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise APIException(f"Не верно задана валюта {quote}")

        try:
            base_ticket = keys[base]
        except KeyError:
            raise APIException(f"Не верно задана валюта {quote}")

        url = f"https://api.apilayer.com/fixer/convert?to={base_ticket}&from={quote_ticket}&amount={amount}"
        r = requests.get(url, headers)
        total = json.loads(r.content)['result']
        return round(total, 2)