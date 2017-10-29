from flask import render_template
from app import app
import requests
import codecs
import json
import datetime
import time
from pathlib import Path
import collections

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

@app.route('/')
@app.route('/index')
@app.route('/index/')
def index():
    results= get_prices(['BTC', 'ETH', 'LTC', 'ETC', 'BCC', 'ZEC', 'XRP', 'NEO', 'DASH', 'IOTA', 'STRAT', 'XMR', 'XLM', 'TRIG'], ['Bitcoin', 'Ethereum', 'Litecoin', 'Ethereum Classic', 'Bitcoin Cash', 'Zcash' ,'Ripple', 'Neo', 'Dash', 'IOTA','Stratis', 'Monero','Stellarlumens', 'Blocksafe']
)
    return render_template('index.html', title='Home', results=results)

@app.route('/about')
@app.route('/about/')
def about():
    return render_template('about.html', title='About Us')


@app.route('/mission')
@app.route('/misson/')
def mission():
    return render_template('mission.html', title='Our Mission')

@app.route('/contact')
@app.route('/contact/')
def contact():
    return render_template('contact.html', title='Contact Us')


@app.route('/careers')
@app.route('/careers/')
def careers():
    return render_template('careers.html', title='Careers')