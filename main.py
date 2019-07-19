from flask import Flask
from flask import Response

# from crawlers.th_stock import fetch_symbols, fetch_nvdr
# from utils import date_utils
# from storages import firestore

# from tasks import *
# from triggers import *

from triggers import trigger_bp


app = Flask(__name__)
app.register_blueprint(trigger_bp)


@app.route('/', methods=['GET'])
def home():
    return Response('Welcome to Wealth AI', status=200)


# @app.route('/fetch/stock/nvdr/', methods=['GET'])
# def fetch_stock_nvdr():
#     last_week, today = date_utils.last_week_pair()
#     stock_nvdr_data = fetch_nvdr(from_date=last_week, to_date=today)
#     firestore.save(
#         collection_name='th_stock_nvdr',
#         data=stock_nvdr_data,
#         id_function=lambda x: '{}-{}'.format(x['symbol'], x['date'].strftime('%Y-%m-%d')))
#     return Response('Saved {} records'.format(len(stock_nvdr_data)), status=200)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
