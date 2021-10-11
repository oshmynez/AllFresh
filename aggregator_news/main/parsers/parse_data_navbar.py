import urllib.error

from bs4 import BeautifulSoup as bs
import requests as req

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}
url = 'https://myfin.by/'

currencies = []


def get_data():
    try:
        response = req.get(url, headers=header)
        soup = bs(response.text, 'lxml')
        tr_currencies = soup.find('table', class_='rate-table__table').find('tr')
        td_currencies = tr_currencies.findAll('td')[1:6]

        for currency in td_currencies:
            value = currency.find('div', class_='currency-block').find('div', class_='currency-block__value').get_text()
            currencies.append(value)

    except BaseException as e:
        print(e.args[0])

    return currencies
