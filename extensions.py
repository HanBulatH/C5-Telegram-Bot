import json
import requests
from configuration import valuts
from configuration import API_KEY

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = valuts[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = valuts[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f"http://api.exchangeratesapi.io/latest??access_key={API_KEY}&base={base_key}&symbols={sym_key}")
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={sym_key}")
        # print(r.content)
        result = json.loads(r.content)[valuts[sym]]
        message = f"Цена {amount} {base} в {sym} : {result}"
        return message