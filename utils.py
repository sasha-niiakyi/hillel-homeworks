import requests

from datetime import datetime
from urllib import parse


def get_currency_iso_code(currency: str) -> int:
    '''
    Функція повертає ISO код валюти
    :param currency: назва валюти
    :return: код валюти
    '''
    currency_dict = {
        'UAH': 980,
        'USD': 840,
        'EUR': 978,
        'GBP': 826,
        'AZN': 944,
        'CAD': 124,
        'PLN': 985,
    }
    try:
        return currency_dict[currency]
    except:
        raise KeyError('Currency not found! Update currencies information')


def get_currency_exchange_rate(currency_a: str,
                               currency_b: str) -> str:
    currency_code_a = get_currency_iso_code(currency_a)
    currency_code_b = get_currency_iso_code(currency_b)

    response = requests.get('https://api.monobank.ua/bank/currency')
    json = response.json()

    if response.status_code == 200:
        for i in range(len(json)):
            if json[i].get('currencyCodeA') == currency_code_a and json[i].get('currencyCodeB') == currency_code_b:
                date = datetime.fromtimestamp(
                    int(json[i].get('date'))
                ).strftime('%Y-%m-%d %H:%M:%S')
                rate_buy = json[i].get('rateBuy')
                rate_sell = json[i].get('rateSell')
                return f'exchange rate {currency_a} to {currency_b} for {date}: \n rate buy - {rate_buy} \n rate sell - {rate_sell}'
            return f'Not found: exchange rate {currency_a} to {currency_b}'
    else:
        return f"Api error {response.status_code}: {json.get('errorDescription')}"


#print(get_currency_exchange_rate('USD', 'UAH'))


def find_delimiter(date: str) -> str:
    if date[2] == date[-5]:
        return date[2]
    else:
        return date[4]


def check_date(rate_date: str) -> str:
    delim = find_delimiter(rate_date)

    formats = ( '%Y' + delim + '%m' + delim + '%d', 
                '%d' + delim + '%m' + delim + '%Y', 
                '%m' + delim + '%d' + delim + '%Y')

    for form in formats:
        try:
            date = datetime.strptime(rate_date, form)
            return f'{date.day:02d}.{date.month:02d}.{date.year}'
        except:
            continue

    return ''



def check_bank(bank: str) -> str:
    '''
    Функція перевіряє написання банку,
    та повертає вірний напис,
    або ничого, якщо такого банку немає
    '''
    if bank in ('nbu', 'nationalbank', 'NationalBank', 'NB', 'NBU'):
        return 'NBU'
    elif bank in ('pb', 'PB', 'privatbank', 'PrivatBank'):
        return 'PB'
    else:
        return ''


def get_pb_exchange_rate(convert_currency: str,
                         bank: str,
                         rate_date: str) -> str:
    params = {
        'json': '',
        'date': rate_date,  # TODO додати функцію валідації формату дати
    }
    query = parse.urlencode(params)
    api_url = 'https://api.privatbank.ua/p24api/exchange_rates?'
    response = requests.get(api_url+query)
    json = response.json()

    if response.status_code == 200:
        rates = json['exchangeRate']
        for rate in rates:
            if rate['currency'] == convert_currency:
                if bank == 'NBU':
                    try:
                        sale_rate = rate['saleRateNB']
                        purchase_rate = rate['purchaseRateNB']
                        return f'Exchange rate UAH to {convert_currency} for {rate_date} at {bank}: sale={sale_rate}, purchase={purchase_rate}'
                    except:
                        return f'There is no exchange rate NBU for {convert_currency}'
                elif bank == 'PB':
                    try:
                        sale_rate = rate['saleRate']
                        purchase_rate = rate['purchaseRate']
                        return f'Exchange rate UAH to {convert_currency} for {rate_date} at {bank}: sale={sale_rate}, purchase={purchase_rate}'
                    except:
                        return f'There is no exchange rate PrivatBank for {convert_currency}'
    else:
        return f'error {response.status_code}'


result = get_pb_exchange_rate('USD', 'PB', '01.11.2022')
print(result)