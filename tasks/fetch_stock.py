from flask import Response

from crawlers.th_stock import fetch_symbols
from main import app
from services import firestore


@app.route('/task/fetch/stock/symbols/', methods=['POST'])
def fetch_stock_symbols():
    stock_symbols_data = fetch_symbols()
    firestore.save(
        collection_name='th_stock_symbols',
        data=stock_symbols_data,
        id_function=lambda x: x['symbol'])
    return Response('Saved {} records'.format(len(stock_symbols_data)), status=200)
