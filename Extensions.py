import requests
import json
from BotUnits import currency, APIKEY


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        quote_lower = quote.lower()
        base_lower = base.lower()
        if quote_lower == base_lower:
            raise APIException(f"Вы ввели одинаковые валюты. Для их перевода ничего делать не надо. \
        Введите новый запрос.")

        try:
            quote_value = currency[quote_lower]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена в базе. Для того чтобы узнать какие валюты доступны \
        для ввода воспользуйтесь командой /value")

        try:
            base_value = currency[base_lower]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена в базе. Для того чтобы узнать какие валюты доступны \
        для ввода воспользуйтесь командой /value")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Введено не корректное значение {amount} для конвертации валют. \
        Введите запрос заново.")

        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={quote_value}{base_value}&key={APIKEY}')
        texts = json.loads(r.content)
        for_currency = float(texts['data'][f'{quote_value}{base_value}'])
        answer = round(for_currency * amount, 2)

        return answer
