import json

from flask import Flask
from flask import Response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return Response('Welcome to Wealth AI', status=200)


@app.route('/fetch/stock/symbols/', methods=['GET'])
def fetch_stock_symbols():
    from crawlers.th_stock import fetch_symbols
    return Response(json.dumps(fetch_symbols()), status=200)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
