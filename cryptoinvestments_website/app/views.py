from app import app
from app import static
import requests
import codecs
import json
import datetime
import time
from pathlib import Path
import collections
from io import StringIO
import matplotlib.pyplot as plt
from flask import Flask, make_response, send_file, render_template, url_for
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


def prices_for_graph(symbol, limit, aggregate):
    r= requests.get('https://min-api.cryptocompare.com/data/histoday?fsym='+ str(symbol) + '&tsym=USD&limit=' +str(limit) + '&aggregate='+ str(aggregate)+ '&e=CCCAGG')
    d = r.json()
    dict = {}
    listOfData = d["Data"]
    for item in listOfData:
        date = datetime.datetime.fromtimestamp(int(item["time"])).strftime('%Y-%m-%d')
        price = int(item["close"])
        dict[date] = price
    return dict

def turn_prices_to_graph(symbol, limit, aggregate, filename):
    d = prices_for_graph(symbol, limit, aggregate)
    days = []
    prices=[]
    counter=1
    for key, value in d.items():
        days.append(counter)
        prices.append(value)
        counter+=1
    plt.plot(prices)
    plt.xlabel('Days')
    plt.ylabel('Prices')
    plt.savefig(filename)



def get_prices(symbols, namesOfCurrency):
    tempsymbols = ','.join(symbols)
    r = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms='+ tempsymbols + '&tsyms=USD')
    tmp= r.json()
    results = collections.OrderedDict()
    i=0
    for symbol in symbols:
        results[namesOfCurrency[i]]=[symbol, tmp['DISPLAY'][str(symbol)]['USD']['PRICE'],tmp['DISPLAY'][str(symbol)]['USD']['CHANGEPCTDAY']]
        i+=1
    return(list(results.items()))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    results= get_prices(['BTC', 'ETH', 'LTC', 'ETC', 'BCC', 'ZEC', 'XRP', 'NEO', 'DASH', 'IOTA'], ['Bitcoin', 'Ethereum', 'Litecoin', 'Ethereum Classic', 'Bitcoin Cash', 'Zcash' ,'Ripple', 'Neo', 'Dash', 'IOTA']
)
    return render_template('index.html', results=results)


@app.route('/about')
@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/mission')
@app.route('/misson/')
def mission():
    return render_template('mission.html')

@app.route('/contact')
@app.route('/contact/')
def contact():
    return render_template('contact.html')


@app.route('/careers')
@app.route('/careers/')
def careers():
    return render_template('careers.html')

@app.route('/index/Bitcoin', methods=['GET', 'POST'])
@app.route('/index/Bitcoin/', methods=['GET', 'POST'])
@app.route('/Bitcoin', methods=['GET', 'POST'])
@app.route('/Bitcoin/', methods=['GET', 'POST'])
def bitcoin():
    results= get_prices(['BTC'],['Bitcoin'])
    turn_prices_to_graph('BTC', 90, 1,'app/static/bitcoin.png')
    return render_template('bitcoin.html',  results = results)

@app.route('/index/Ethereum', methods=['GET', 'POST'])
@app.route('/index/Ethereum/', methods=['GET', 'POST'])
@app.route('/Ethereum', methods=['GET', 'POST'])
@app.route('/Ethereum/', methods=['GET', 'POST'])
def ethereum():
    results= get_prices(['ETH'],['Ethereum'])
    turn_prices_to_graph('ETH', 90, 1,'app/static/Ethereum.png')
    return render_template('ethereum.html', results = results)


@app.route('/index/Ethereum Classic', methods=['GET', 'POST'])
@app.route('/index/Ethereum Classic/', methods=['GET', 'POST'])
@app.route('/Ethereum Classic', methods=['GET', 'POST'])
@app.route('/Ethereum Classic/', methods=['GET', 'POST'])
def ethereum_classic():
    results= get_prices(['ETC'],['Ethereum Classic'])
    turn_prices_to_graph('ETC', 90, 1,'app/static/Ethereum_Classic.png')
    return render_template('ethereum_classic.html', results = results)

@app.route('/index/Litecoin', methods=['GET', 'POST'])
@app.route('/index/Litecoin/', methods=['GET', 'POST'])
@app.route('/Litecoin', methods=['GET', 'POST'])
@app.route('/Litecoin/', methods=['GET', 'POST'])
def litecoin():
    results= get_prices(['LTC'],['Litecoin'])
    turn_prices_to_graph('LTC', 90, 1,'app/static/litecoin.png')
    return render_template('litecoin.html', results = results)

@app.route('/index/Bitcoin Cash', methods=['GET', 'POST'])
@app.route('/index/Bitcoin Cash/', methods=['GET', 'POST'])
@app.route('/Bitcoin Cash', methods=['GET', 'POST'])
@app.route('/Bitcoin Cash/', methods=['GET', 'POST'])
def bitcoin_cash():
    results= get_prices(['BCC'],['Bitcoin_Cash'])
    turn_prices_to_graph('BCC', 90, 1,'app/static/bitcoin_cash.png')
    return render_template('bitcoin_cash.html', results = results)

@app.route('/index/Zcash', methods=['GET', 'POST'])
@app.route('/index/Zcash/', methods=['GET', 'POST'])
@app.route('/Zcash', methods=['GET', 'POST'])
@app.route('/Zcash/', methods=['GET', 'POST'])
def zcash():
    results= get_prices(['ZEC'],['Zcash'])
    turn_prices_to_graph('ZEC', 90, 1,'app/static/Zcash.png')
    return render_template('zcash.html', results = results)

@app.route('/index/Ripple', methods=['GET', 'POST'])
@app.route('/index/Ripple/', methods=['GET', 'POST'])
@app.route('/Ripple', methods=['GET', 'POST'])
@app.route('/Ripple/', methods=['GET', 'POST'])
def ripple():
    results= get_prices(['XRP'],['Ripple'])
    turn_prices_to_graph('XRP', 90, 1,'app/static/ripple.png')
    return render_template('ripple.html', results = results)

@app.route('/index/Neo', methods=['GET', 'POST'])
@app.route('/index/Neo/', methods=['GET', 'POST'])
@app.route('/Neo', methods=['GET', 'POST'])
@app.route('/Neo/', methods=['GET', 'POST'])
def neo():
    results= get_prices(['NEO'],['Neo'])
    turn_prices_to_graph('NEO', 90, 1,'app/static/neo.png')
    return render_template('neo.html', results = results)

@app.route('/index/Dash', methods=['GET', 'POST'])
@app.route('/index/Dash/', methods=['GET', 'POST'])
@app.route('/Dash', methods=['GET', 'POST'])
@app.route('/Dash/', methods=['GET', 'POST'])
def dash():
    results= get_prices(['DASH'],['Dash'])
    turn_prices_to_graph('DASH', 90, 1,'app/static/dash.png')
    return render_template('dash.html', results = results)

@app.route('/index/IOTA', methods=['GET', 'POST'])
@app.route('/index/IOTA/', methods=['GET', 'POST'])
@app.route('/IOTA', methods=['GET', 'POST'])
@app.route('/IOTA/', methods=['GET', 'POST'])
def iota():
    results= get_prices(['IOTA'],['IOTA'])
    turn_prices_to_graph('IOTA', 90, 1,'app/static/iota.png')
    return render_template('iota.html', results = results)





'''
@app.route('/static/bitcoin.png/')
def bitcoin_graph():
    img = plt.savefig('app/static/bitcoin.png')
    return send_file(img, mimetype='image/png')
'''




