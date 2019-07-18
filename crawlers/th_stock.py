import requests
from lxml import etree


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
