from flask import Flask
from flask import Response

from crawlers.th_stock import fetch_symbols, fetch_nvdr
from utils import date_utils
from storages import firestore


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return Response('Welcome to Wealth AI', status=200)


@app.route('/fetch/stock/symbols/', methods=['GET'])
def fetch_stock_symbols():
    stock_symbols_data = fetch_symbols()
    firestore.save(
        collection_name='th_stock_symbols',
        data=stock_symbols_data,
        id_function=lambda x: x['symbol'])
    return Response('Saved {} records'.format(len(stock_symbols_data)), status=200)


@app.route('/fetch/stock/nvdr/', methods=['GET'])
def fetch_stock_nvdr():
    last_week, today = date_utils.last_week_pair()
    stock_nvdr_data = fetch_nvdr(from_date=last_week, to_date=today)
    firestore.save(
        collection_name='th_stock_nvdr',
        data=stock_nvdr_data,
        id_function=lambda x: '{}-{}'.format(x['symbol'], x['date'].strftime('%Y-%m-%d')))
    return Response('Saved {} records'.format(len(stock_nvdr_data)), status=200)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
