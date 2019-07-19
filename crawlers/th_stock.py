import requests

from datetime import datetime, timedelta
from lxml import etree

from utils import date_utils, string_utils


def fetch_symbols():
    response = requests.get('https://www.set.or.th/dat/eod/listedcompany/static/listedCompanies_th_TH.xls')
    encoded_content = response.content.decode('iso-8859-11').encode('utf-8')
    response_tree = etree.HTML(encoded_content)

    # Fetch all symbols
    set_symbols = []
    for row in response_tree.xpath('//table[1]/tr[position()>2]'):
        market = row.xpath('td[3]')[0].text.strip()
        if market == 'SET':
            set_symbols.append(row.xpath('td[1]')[0].text.strip())

    def _parse_index_page(response_content):
        response_tree = etree.HTML(response_content)
        symbols = set()
        for row in response_tree.xpath('//table')[2].xpath('tbody/tr/td[position()=1]/a'):
            symbols.add(row.text.strip())
        return symbols

    # Fetch SET50
    response = requests.get(
        'https://marketdata.set.or.th/mkt/sectorquotation.do?market=SET&sector=SET50&language=th&country=TH')
    set50_symbols = _parse_index_page(response.content)

    # Fetch SET100
    response = requests.get(
        'https://marketdata.set.or.th/mkt/sectorquotation.do?market=SET&sector=SET100&language=th&country=TH')
    set100_symbols = _parse_index_page(response.content)

    symbols = []
    for symbol in set_symbols:
        symbols.append({
            'symbol': symbol,
            'set50': symbol in set50_symbols,
            'set100': symbol in set100_symbols,
        })

    return symbols


def fetch_nvdr(from_date, to_date=None):
    if not to_date:
        to_date = datetime.today()

    to_date = date_utils.strip_time(to_date)
    from_date = date_utils.strip_time(from_date)

    crawl_date = from_date
    nvdr_data = []

    while crawl_date <= to_date:
        request_url = 'https://www.set.or.th/set/nvdrbystock.do?format=excel&date={}'.format(
            crawl_date.strftime('%d/%m/%Y'))
        response = requests.get(request_url)

        response_tree = etree.HTML(response.content)
        tds = response_tree.xpath('//table[2]/tr[position()>2]/td')

        for x in range(0, len(tds), 11):  # 11 => cells per row
            row = tds[x:x + 11]
            nvdr_data.append({
                'symbol': row[0].text,
                'date': crawl_date,
                'buy_volume': string_utils.clean_num_string(row[1].text),  # Volume Buy
                'sell_volume': string_utils.clean_num_string(row[2].text),  # Volume Sell
                'buy_value': string_utils.clean_num_string(row[6].text),  # Value Buy
                'sell_value': string_utils.clean_num_string(row[7].text),  # Value Sell
                'percentage': string_utils.clean_num_string(row[5].text),  # Percentage
            })

        crawl_date = crawl_date + timedelta(days=1)

    return nvdr_data
