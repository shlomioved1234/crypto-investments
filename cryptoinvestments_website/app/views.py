from app import app
import os.path
#from app import static
import requests
import codecs
import json
import datetime
import time
#from pathlib import Path
import collections
from io import StringIO
import matplotlib.pyplot as plt
from flask import Flask, make_response, send_file, render_template, url_for, request, flash, redirect
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import fnmatch








                         
        

def prices_for_graph(symbol, limit, aggregate):
    r= requests.get('https://min-api.cryptocompare.com/data/histoday?fsym='+ str(symbol) + '&tsym=USD&limit=' +str(limit) + '&aggregate='+ str(aggregate)+ '&e=CCCAGG')
    d = r.json()
    dict = collections.OrderedDict()
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
    if (limit == 7):
        x = [0, 2, 5,  7]
    if (limit == 30):
        x = [0, 15, 30]
    if (limit == 60):
        x = [0, 20, 40, 60]
    if (limit == 90):
        x = [0, 25, 45, 65, 90]
    counter=1
    for key, value in d.items():
        days.append(key)
        prices.append(value)
        counter+=1
    x = np.array(x)
    if (limit == 7):
        days=[days[0], days[2], days[5],  days[7]]
    if (limit == 30):
        days=[days[0], days[15],  days[30]]
    if (limit == 60):
        days=[days[0], days[20],  days[40], days[60]]
    if (limit == 90):
        days=[days[0], days[25], days[45], days[65], days[90]]
    plt.xticks(x, days)
    plt.plot(prices)
    plt.title(symbol)
    plt.xlabel('Days')
    plt.ylabel('Prices')
    plt.savefig(filename)
    plt.clf()



def get_prices(symbols, namesOfCurrency):
    tempsymbols = ','.join(symbols)
    r = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms='+ tempsymbols + '&tsyms=USD')
    tmp= r.json()
    results = collections.OrderedDict()
    i=0
    for symbol in symbols:
        results[namesOfCurrency[i]]={'name':symbol, 'price' : tmp['DISPLAY'][str(symbol)]['USD']['PRICE'], 'percentchange':tmp['DISPLAY'][str(symbol)]['USD']['CHANGEPCTDAY'], 'rawmarketcap':tmp['RAW'][str(symbol)]['USD']['MKTCAP'], 'marketcap':tmp['DISPLAY'][str(symbol)]['USD']['MKTCAP']}
        i+=1
    d_descending = collections.OrderedDict(sorted(results.items(), key=lambda kv: kv[1]['rawmarketcap'], reverse=True))
    return(d_descending)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    results= get_prices(['BTC', 'ETH', 'LTC', 'ETC', 'BCC', 'ZEC', 'XRP', 'NEO', 'DASH', 'IOTA', 'EOS', 'XCP', 'NEOS', 'XMR', 'LSK', 'GNT', 'WAVES', 'SNT', 'STRAT', 'VTC', 'XVG', 'DOGE', 'SC', 'ADA', 'SBD', 'BTS', 'GAS', 'REP', 'FCT', 'XLM', 'XEM', 'STEEM', 'PIVX', 'STORJ', 'DCR', 'XZC', 'SYS', 'MAID', 'LBC', 'OK', 'BNT'], ['Bitcoin', 'Ethereum', 'Litecoin', 'Ethereum Classic', 'Bitcoin Cash', 'Zcash' ,'Ripple', 'Neo', 'Dash', 'IOTA', 'EOS', 'Counterparty', 'Neoscoin', 'Monero', 'Lisk', 'Golem', 'Waves', 'Status','Stratis', 'Vertcoin', 'Verge', 'Dogecoin', 'Siacoin', 'Cardano', 'Steem Dollars', 'Bitshares', 'Gas', 'Augur', 'Factom', 'Stellar Lumens', 'Nem', 'Steem', 'Pivx', 'Storj', 'Decred', 'ZCoin', 'Syscoin', 'MaidSafeCoin', 'LBRY Credits', 'OKCash', 'Bancor Network'])
    #sentiment=collections.OrderedDict()
    #for key,value in results.items():
    #    sentiment[key]=get_comments_and_sentiment(key)
    return render_template('index.html', results=results.items())#, sentiment=sentiment.items())


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
    turn_prices_to_graph('BTC', 7, 1,'app/static/bitcoin_7.png')
    turn_prices_to_graph('BTC', 30, 1,'app/static/bitcoin_30.png')
    turn_prices_to_graph('BTC', 60, 1,'app/static/bitcoin_60.png')
    turn_prices_to_graph('BTC', 90, 1,'app/static/bitcoin_90.png')
    return render_template('bitcoin.html',  results = results.items())

@app.route('/index/Ethereum', methods=['GET', 'POST'])
@app.route('/index/Ethereum/', methods=['GET', 'POST'])
@app.route('/Ethereum', methods=['GET', 'POST'])
@app.route('/Ethereum/', methods=['GET', 'POST'])
def ethereum():
    results= get_prices(['ETH'],['Ethereum'])
    turn_prices_to_graph('ETH', 7, 1,'app/static/ethereum_7.png')
    turn_prices_to_graph('ETH', 30, 1,'app/static/ethereum_30.png')
    turn_prices_to_graph('ETH', 60, 1,'app/static/ethereum_60.png')
    turn_prices_to_graph('ETH', 90, 1,'app/static/ethereum_90.png')
    return render_template('ethereum.html', results = results.items())


@app.route('/index/Ethereum Classic', methods=['GET', 'POST'])
@app.route('/index/Ethereum Classic/', methods=['GET', 'POST'])
@app.route('/Ethereum Classic', methods=['GET', 'POST'])
@app.route('/Ethereum Classic/', methods=['GET', 'POST'])
def ethereum_classic():
    results= get_prices(['ETC'],['Ethereum Classic'])
    turn_prices_to_graph('ETC', 7, 1,'app/static/ethereum_classic_7.png')
    turn_prices_to_graph('ETC', 30, 1,'app/static/ethereum_classic_30.png')
    turn_prices_to_graph('ETC', 60, 1,'app/static/ethereum_classic_60.png')
    turn_prices_to_graph('ETC', 90, 1,'app/static/ethereum_classic_90.png')
    return render_template('ethereum_classic.html', results = results.items())

@app.route('/index/Litecoin', methods=['GET', 'POST'])
@app.route('/index/Litecoin/', methods=['GET', 'POST'])
@app.route('/Litecoin', methods=['GET', 'POST'])
@app.route('/Litecoin/', methods=['GET', 'POST'])
def litecoin():
    results= get_prices(['LTC'],['Litecoin'])
    turn_prices_to_graph('LTC', 7, 1,'app/static/litecoin_7.png')
    turn_prices_to_graph('LTC', 30, 1,'app/static/litecoin_30.png')
    turn_prices_to_graph('LTC', 60, 1,'app/static/litecoin_60.png')
    turn_prices_to_graph('LTC', 90, 1,'app/static/litecoin_90.png')
    return render_template('litecoin.html', results = results.items())

@app.route('/index/Bitcoin Cash', methods=['GET', 'POST'])
@app.route('/index/Bitcoin Cash/', methods=['GET', 'POST'])
@app.route('/Bitcoin Cash', methods=['GET', 'POST'])
@app.route('/Bitcoin Cash/', methods=['GET', 'POST'])
def bitcoin_cash():
    results= get_prices(['BCC'],['Bitcoin_Cash'])
    turn_prices_to_graph('BCC', 7, 1,'app/static/bitcoin_cash_7.png')
    turn_prices_to_graph('BCC', 30, 1,'app/static/bitcoin_cash_30.png')
    turn_prices_to_graph('BCC', 60, 1,'app/static/bitcoin_cash_60.png')
    turn_prices_to_graph('BCC', 90, 1,'app/static/bitcoin_cash_90.png')
    return render_template('bitcoin_cash.html', results = results.items())

@app.route('/index/Zcash', methods=['GET', 'POST'])
@app.route('/index/Zcash/', methods=['GET', 'POST'])
@app.route('/Zcash', methods=['GET', 'POST'])
@app.route('/Zcash/', methods=['GET', 'POST'])
def zcash():
    results= get_prices(['ZEC'],['Zcash'])
    turn_prices_to_graph('ZEC', 7, 1,'app/static/zcash_7.png')
    turn_prices_to_graph('ZEC', 30, 1,'app/static/zcash_30.png')
    turn_prices_to_graph('ZEC', 60, 1,'app/static/zcash_60.png')
    turn_prices_to_graph('ZEC', 90, 1,'app/static/zcash_90.png')
    return render_template('zcash.html', results = results.items())

@app.route('/index/Ripple', methods=['GET', 'POST'])
@app.route('/index/Ripple/', methods=['GET', 'POST'])
@app.route('/Ripple', methods=['GET', 'POST'])
@app.route('/Ripple/', methods=['GET', 'POST'])
def ripple():
    results= get_prices(['XRP'],['Ripple'])
    turn_prices_to_graph('XRP', 7, 1,'app/static/ripple_7.png')
    turn_prices_to_graph('XRP', 30, 1,'app/static/ripple_30.png')
    turn_prices_to_graph('XRP', 60, 1,'app/static/ripple_60.png')
    turn_prices_to_graph('XRP', 90, 1,'app/static/ripple_90.png')
    return render_template('ripple.html', results = results.items())

@app.route('/index/Neo', methods=['GET', 'POST'])
@app.route('/index/Neo/', methods=['GET', 'POST'])
@app.route('/Neo', methods=['GET', 'POST'])
@app.route('/Neo/', methods=['GET', 'POST'])
def neo():
    results= get_prices(['NEO'],['Neo'])
    turn_prices_to_graph('NEO', 7, 1,'app/static/neo_7.png')
    turn_prices_to_graph('NEO', 30, 1,'app/static/neo_30.png')
    turn_prices_to_graph('NEO', 60, 1,'app/static/neo_60.png')
    turn_prices_to_graph('NEO', 90, 1,'app/static/neo_90.png')
    return render_template('neo.html', results = results.items())

@app.route('/index/Dash', methods=['GET', 'POST'])
@app.route('/index/Dash/', methods=['GET', 'POST'])
@app.route('/Dash', methods=['GET', 'POST'])
@app.route('/Dash/', methods=['GET', 'POST'])
def dash():
    results= get_prices(['DASH'],['Dash'])
    turn_prices_to_graph('DASH', 7, 1,'app/static/dash_7.png')
    turn_prices_to_graph('DASH', 30, 1,'app/static/dash_30.png')
    turn_prices_to_graph('DASH', 60, 1,'app/static/dash_60.png')
    turn_prices_to_graph('DASH', 90, 1,'app/static/dash_90.png')
    return render_template('dash.html', results = results.items())

@app.route('/index/IOTA', methods=['GET', 'POST'])
@app.route('/index/IOTA/', methods=['GET', 'POST'])
@app.route('/IOTA', methods=['GET', 'POST'])
@app.route('/IOTA/', methods=['GET', 'POST'])
def iota():
    results= get_prices(['IOTA'],['IOTA'])
    turn_prices_to_graph('IOTA', 7, 1,'app/static/iota_7.png')
    turn_prices_to_graph('IOTA', 30, 1,'app/static/iota_30.png')
    turn_prices_to_graph('IOTA', 60, 1,'app/static/iota_60.png')
    turn_prices_to_graph('IOTA', 90, 1,'app/static/iota_90.png')
    return render_template('iota.html', results = results.items())

@app.route('/index/EOS', methods=['GET', 'POST'])
@app.route('/index/EOS/', methods=['GET', 'POST'])
@app.route('/EOS', methods=['GET', 'POST'])
@app.route('/EOS/', methods=['GET', 'POST'])
def eos():
    results= get_prices(['EOS'],['EOS'])
    turn_prices_to_graph('EOS', 7, 1,'app/static/eos_7.png')
    turn_prices_to_graph('EOS', 30, 1,'app/static/eos_30.png')
    turn_prices_to_graph('EOS', 60, 1,'app/static/eos_60.png')
    turn_prices_to_graph('EOS', 90, 1,'app/static/eos_90.png')
    return render_template('eos.html', results = results.items())

@app.route('/index/Counterparty', methods=['GET', 'POST'])
@app.route('/index/Counterparty/', methods=['GET', 'POST'])
@app.route('/Counterparty', methods=['GET', 'POST'])
@app.route('/Counterparty/', methods=['GET', 'POST'])
def counterparty():
    results= get_prices(['XCP'],['Counterparty'])
    turn_prices_to_graph('XCP', 7, 1,'app/static/counterparty_7.png')
    turn_prices_to_graph('XCP', 30, 1,'app/static/counterparty_30.png')
    turn_prices_to_graph('XCP', 60, 1,'app/static/counterparty_60.png')
    turn_prices_to_graph('XCP', 90, 1,'app/static/counterparty_90.png')
    return render_template('counterparty.html', results = results.items())

@app.route('/index/Neoscoin', methods=['GET', 'POST'])
@app.route('/index/Neoscoin/', methods=['GET', 'POST'])
@app.route('/Neoscoin', methods=['GET', 'POST'])
@app.route('/Neoscoin/', methods=['GET', 'POST'])
def neoscoin():
    results= get_prices(['NEOS'],['Neoscoin'])
    turn_prices_to_graph('NEOS', 7, 1,'app/static/neoscoin_7.png')
    turn_prices_to_graph('NEOS', 30, 1,'app/static/neoscoin_30.png')
    turn_prices_to_graph('NEOS', 60, 1,'app/static/neoscoin_60.png')
    turn_prices_to_graph('NEOS', 90, 1,'app/static/neoscoin_90.png')
    return render_template('neoscoin.html', results = results.items())

@app.route('/index/Monero', methods=['GET', 'POST'])
@app.route('/index/Monero/', methods=['GET', 'POST'])
@app.route('/Monero', methods=['GET', 'POST'])
@app.route('/Monero/', methods=['GET', 'POST'])
def monero():
    results= get_prices(['XMR'],['Monero'])
    turn_prices_to_graph('XMR', 7, 1,'app/static/monero_7.png')
    turn_prices_to_graph('XMR', 30, 1,'app/static/monero_30.png')
    turn_prices_to_graph('XMR', 60, 1,'app/static/monero_60.png')
    turn_prices_to_graph('XMR', 90, 1,'app/static/monero_90.png')
    return render_template('monero.html', results = results.items())

@app.route('/index/Lisk', methods=['GET', 'POST'])
@app.route('/index/Lisk/', methods=['GET', 'POST'])
@app.route('/Lisk', methods=['GET', 'POST'])
@app.route('/Lisk/', methods=['GET', 'POST'])
def lisk():
    results= get_prices(['LSK'],['Lisk'])
    turn_prices_to_graph('LSK', 7, 1,'app/static/lisk_7.png')
    turn_prices_to_graph('LSK', 30, 1,'app/static/lisk_30.png')
    turn_prices_to_graph('LSK', 60, 1,'app/static/lisk_60.png')
    turn_prices_to_graph('LSK', 90, 1,'app/static/lisk_90.png')
    return render_template('lisk.html', results = results.items())

@app.route('/index/Golem', methods=['GET', 'POST'])
@app.route('/index/Golem/', methods=['GET', 'POST'])
@app.route('/Golem', methods=['GET', 'POST'])
@app.route('/Golem/', methods=['GET', 'POST'])
def golem():
    results= get_prices(['GNT'],['Golem'])
    turn_prices_to_graph('GNT', 7, 1,'app/static/golem_7.png')
    turn_prices_to_graph('GNT', 30, 1,'app/static/golem_30.png')
    turn_prices_to_graph('GNT', 60, 1,'app/static/golem_60.png')
    turn_prices_to_graph('GNT', 90, 1,'app/static/golem_90.png')
    return render_template('golem.html', results = results.items())

@app.route('/index/Waves', methods=['GET', 'POST'])
@app.route('/index/Waves/', methods=['GET', 'POST'])
@app.route('/Waves', methods=['GET', 'POST'])
@app.route('/Waves/', methods=['GET', 'POST'])
def waves():
    results= get_prices(['WAVES'],['Waves'])
    turn_prices_to_graph('WAVES', 7, 1,'app/static/waves_7.png')
    turn_prices_to_graph('WAVES', 30, 1,'app/static/waves_30.png')
    turn_prices_to_graph('WAVES', 60, 1,'app/static/waves_60.png')
    turn_prices_to_graph('WAVES', 90, 1,'app/static/waves_90.png')
    return render_template('waves.html', results = results.items())

@app.route('/index/Status', methods=['GET', 'POST'])
@app.route('/index/Status/', methods=['GET', 'POST'])
@app.route('/Status', methods=['GET', 'POST'])
@app.route('/Status/', methods=['GET', 'POST'])
def status():
    results= get_prices(['SNT'],['Status'])
    turn_prices_to_graph('SNT', 7, 1,'app/static/status_7.png')
    turn_prices_to_graph('SNT', 30, 1,'app/static/status_30.png')
    turn_prices_to_graph('SNT', 60, 1,'app/static/status_60.png')
    turn_prices_to_graph('SNT', 90, 1,'app/static/status_90.png')
    return render_template('status.html', results = results.items())

@app.route('/index/Stratis', methods=['GET', 'POST'])
@app.route('/index/Stratis/', methods=['GET', 'POST'])
@app.route('/Stratis', methods=['GET', 'POST'])
@app.route('/Stratis/', methods=['GET', 'POST'])
def stratis():
    results= get_prices(['STRAT'],['Stratis'])
    turn_prices_to_graph('STRAT', 7, 1,'app/static/stratis_7.png')
    turn_prices_to_graph('STRAT', 30, 1,'app/static/stratis_30.png')
    turn_prices_to_graph('STRAT', 60, 1,'app/static/stratis_60.png')
    turn_prices_to_graph('STRAT', 90, 1,'app/static/stratis_90.png')
    return render_template('stratis.html', results = results.items())

@app.route('/index/Vertcoin', methods=['GET', 'POST'])
@app.route('/index/Vertcoin/', methods=['GET', 'POST'])
@app.route('/Vertcoin', methods=['GET', 'POST'])
@app.route('/Vertcoin/', methods=['GET', 'POST'])
def vertcoin():
    results= get_prices(['VTC'],['Vertcoin'])
    turn_prices_to_graph('VTC', 7, 1,'app/static/vertcoin_7.png')
    turn_prices_to_graph('VTC', 30, 1,'app/static/vertcoin_30.png')
    turn_prices_to_graph('VTC', 60, 1,'app/static/vertcoin_60.png')
    turn_prices_to_graph('VTC', 90, 1,'app/static/vertcoin_90.png')
    return render_template('vertcoin.html', results = results.items())

@app.route('/index/Verge', methods=['GET', 'POST'])
@app.route('/index/Verge/', methods=['GET', 'POST'])
@app.route('/Verge', methods=['GET', 'POST'])
@app.route('/Verge/', methods=['GET', 'POST'])
def verge():
    results= get_prices(['XVG'],['Stratis'])
    turn_prices_to_graph('XVG', 7, 1,'app/static/verge_7.png')
    turn_prices_to_graph('XVG', 30, 1,'app/static/verge_30.png')
    turn_prices_to_graph('XVG', 60, 1,'app/static/verge_60.png')
    turn_prices_to_graph('XVG', 90, 1,'app/static/verge_90.png')
    return render_template('verge.html', results = results.items())

@app.route('/index/Dogecoin', methods=['GET', 'POST'])
@app.route('/index/Dogecoin/', methods=['GET', 'POST'])
@app.route('/Dogecoin', methods=['GET', 'POST'])
@app.route('/Dogecoin/', methods=['GET', 'POST'])
def dogecoin():
    results= get_prices(['DOGE'],['Dogecoin'])
    turn_prices_to_graph('DOGE', 7, 1,'app/static/dogecoin_7.png')
    turn_prices_to_graph('DOGE', 30, 1,'app/static/dogecoin_30.png')
    turn_prices_to_graph('DOGE', 60, 1,'app/static/dogecoin_60.png')
    turn_prices_to_graph('DOGE', 90, 1,'app/static/dogecoin_90.png')
    return render_template('dogecoin.html', results = results.items())

@app.route('/index/Siacoin', methods=['GET', 'POST'])
@app.route('/index/Siacoin/', methods=['GET', 'POST'])
@app.route('/Siacoin', methods=['GET', 'POST'])
@app.route('/Siacoin/', methods=['GET', 'POST'])
def siacoin():
    results= get_prices(['SC'],['Siacoin'])
    turn_prices_to_graph('SC', 7, 1,'app/static/siacoin_7.png')
    turn_prices_to_graph('SC', 30, 1,'app/static/siacoin_30.png')
    turn_prices_to_graph('SC', 60, 1,'app/static/siacoin_60.png')
    turn_prices_to_graph('SC', 90, 1,'app/static/siacoin_90.png')
    return render_template('siacoin.html', results = results.items())

@app.route('/index/Cardano', methods=['GET', 'POST'])
@app.route('/index/Cardano/', methods=['GET', 'POST'])
@app.route('/Cardano', methods=['GET', 'POST'])
@app.route('/Cardano/', methods=['GET', 'POST'])
def cardano():
    results= get_prices(['ADA'],['Cardano'])
    turn_prices_to_graph('ADA', 7, 1,'app/static/cardano_7.png')
    turn_prices_to_graph('ADA', 30, 1,'app/static/cardano_30.png')
    turn_prices_to_graph('ADA', 60, 1,'app/static/cardano_60.png')
    turn_prices_to_graph('ADA', 90, 1,'app/static/cardano_90.png')
    return render_template('cardano.html', results = results.items())

@app.route('/index/Steem Dollars', methods=['GET', 'POST'])
@app.route('/index/Steem Dollars/', methods=['GET', 'POST'])
@app.route('/Steem Dollars', methods=['GET', 'POST'])
@app.route('/Steem Dollars/', methods=['GET', 'POST'])
def steem_dollars():
    results= get_prices(['SBD'],['Steem Dollars'])
    turn_prices_to_graph('SBD', 7, 1,'app/static/steem_dollars_7.png')
    turn_prices_to_graph('SBD', 30, 1,'app/static/steem_dollars_30.png')
    turn_prices_to_graph('SBD', 60, 1,'app/static/steem_dollars_60.png')
    turn_prices_to_graph('SBD', 90, 1,'app/static/steem_dollars_90.png')
    return render_template('steem_dollars.html', results = results.items())

@app.route('/index/Bitshares', methods=['GET', 'POST'])
@app.route('/index/Bitshares/', methods=['GET', 'POST'])
@app.route('/Bitshares', methods=['GET', 'POST'])
@app.route('/Bitshares/', methods=['GET', 'POST'])
def bitshares():
    results= get_prices(['BTS'],['Bitshares'])
    turn_prices_to_graph('BTS', 7, 1,'app/static/bitshares_7.png')
    turn_prices_to_graph('BTS', 30, 1,'app/static/bitshares_30.png')
    turn_prices_to_graph('BTS', 60, 1,'app/static/bitshares_60.png')
    turn_prices_to_graph('BTS', 90, 1,'app/static/bitshares_90.png')
    return render_template('bitshares.html', results = results.items())

@app.route('/index/Gas', methods=['GET', 'POST'])
@app.route('/index/Gas/', methods=['GET', 'POST'])
@app.route('/Gas', methods=['GET', 'POST'])
@app.route('/Gas/', methods=['GET', 'POST'])
def gas():
    results= get_prices(['GAS'],['Gas'])
    turn_prices_to_graph('GAS', 7, 1,'app/static/gas_7.png')
    turn_prices_to_graph('GAS', 30, 1,'app/static/gas_30.png')
    turn_prices_to_graph('GAS', 60, 1,'app/static/gas_60.png')
    turn_prices_to_graph('GAS', 90, 1,'app/static/gas_90.png')
    return render_template('gas.html', results = results.items())

@app.route('/index/Augur', methods=['GET', 'POST'])
@app.route('/index/Augur/', methods=['GET', 'POST'])
@app.route('/Augur', methods=['GET', 'POST'])
@app.route('/Augur/', methods=['GET', 'POST'])
def augur():
    results= get_prices(['REP'],['Augur'])
    turn_prices_to_graph('REP', 7, 1,'app/static/augur_7.png')
    turn_prices_to_graph('REP', 30, 1,'app/static/augur_30.png')
    turn_prices_to_graph('REP', 60, 1,'app/static/augur_60.png')
    turn_prices_to_graph('REP', 90, 1,'app/static/augur_90.png')
    return render_template('augur.html', results = results.items())

@app.route('/index/Stellar Lumens', methods=['GET', 'POST'])
@app.route('/index/Stellar Lumens/', methods=['GET', 'POST'])
@app.route('/Stellar Lumens', methods=['GET', 'POST'])
@app.route('/Stellar Lumens/', methods=['GET', 'POST'])
def stellar_lumens():
    results= get_prices(['XLM'],['Stellar Lumens'])
    turn_prices_to_graph('XLM', 7, 1,'app/static/stellar_lumens_7.png')
    turn_prices_to_graph('XLM', 30, 1,'app/static/stellar_lumens_30.png')
    turn_prices_to_graph('XLM', 60, 1,'app/static/stellar_lumens_60.png')
    turn_prices_to_graph('XLM', 90, 1,'app/static/stellar_lumens_90.png')
    return render_template('stellar_lumens.html', results = results.items())

@app.route('/index/Factom', methods=['GET', 'POST'])
@app.route('/index/Factom/', methods=['GET', 'POST'])
@app.route('/Factom', methods=['GET', 'POST'])
@app.route('/Factom/', methods=['GET', 'POST'])
def factom():
    results= get_prices(['FCT'],['Factom'])
    turn_prices_to_graph('FCT', 7, 1,'app/static/factom_7.png')
    turn_prices_to_graph('FCT', 30, 1,'app/static/factom_30.png')
    turn_prices_to_graph('FCT', 60, 1,'app/static/factom_60.png')
    turn_prices_to_graph('FCT', 90, 1,'app/static/factom_90.png')
    return render_template('factom.html', results = results.items())

@app.route('/index/Nem', methods=['GET', 'POST'])
@app.route('/index/Nem/', methods=['GET', 'POST'])
@app.route('/Nem', methods=['GET', 'POST'])
@app.route('/Nem/', methods=['GET', 'POST'])
def nem():
    results= get_prices(['XEM'],['Nem'])
    turn_prices_to_graph('XEM', 7, 1,'app/static/nem_7.png')
    turn_prices_to_graph('XEM', 30, 1,'app/static/nem_30.png')
    turn_prices_to_graph('XEM', 60, 1,'app/static/nem_60.png')
    turn_prices_to_graph('XEM', 90, 1,'app/static/nem_90.png')
    return render_template('nem.html', results = results.items())

@app.route('/index/Steem', methods=['GET', 'POST'])
@app.route('/index/Steem/', methods=['GET', 'POST'])
@app.route('/Steem', methods=['GET', 'POST'])
@app.route('/Steem/', methods=['GET', 'POST'])
def steem():
    results= get_prices(['STEEM'],['Steem'])
    turn_prices_to_graph('STEEM', 7, 1,'app/static/steem_7.png')
    turn_prices_to_graph('STEEM', 30, 1,'app/static/steem_30.png')
    turn_prices_to_graph('STEEM', 60, 1,'app/static/steem_60.png')
    turn_prices_to_graph('STEEM', 90, 1,'app/static/steem_90.png')
    return render_template('steem.html', results = results.items())

@app.route('/index/Pivx', methods=['GET', 'POST'])
@app.route('/index/Pivx/', methods=['GET', 'POST'])
@app.route('/Pivx', methods=['GET', 'POST'])
@app.route('/Pivx/', methods=['GET', 'POST'])
def pivx():
    results= get_prices(['PIVX'],['Pivx'])
    turn_prices_to_graph('PIVX', 7, 1,'app/static/pivx_7.png')
    turn_prices_to_graph('PIVX', 30, 1,'app/static/pivx_30.png')
    turn_prices_to_graph('PIVX', 60, 1,'app/static/pivx_60.png')
    turn_prices_to_graph('PIVX', 90, 1,'app/static/pivx_90.png')
    return render_template('pivx.html', results = results.items())

@app.route('/index/Storj', methods=['GET', 'POST'])
@app.route('/index/Storj/', methods=['GET', 'POST'])
@app.route('/Storj', methods=['GET', 'POST'])
@app.route('/Storj/', methods=['GET', 'POST'])
def storj():
    results= get_prices(['STORJ'],['Storj'])
    turn_prices_to_graph('STORJ', 7, 1,'app/static/storj_7.png')
    turn_prices_to_graph('STORJ', 30, 1,'app/static/storj_30.png')
    turn_prices_to_graph('STORJ', 60, 1,'app/static/storj_60.png')
    turn_prices_to_graph('STORJ', 90, 1,'app/static/storj_90.png')
    return render_template('storj.html', results = results.items())


@app.route('/index/Decred', methods=['GET', 'POST'])
@app.route('/index/Decred/', methods=['GET', 'POST'])
@app.route('/Decred', methods=['GET', 'POST'])
@app.route('/Decred/', methods=['GET', 'POST'])
def decred():
    results= get_prices(['DCR'],['Decred'])
    turn_prices_to_graph('DCR', 7, 1,'app/static/decred_7.png')
    turn_prices_to_graph('DCR', 30, 1,'app/static/decred_30.png')
    turn_prices_to_graph('DCR', 60, 1,'app/static/decred_60.png')
    turn_prices_to_graph('DCR', 90, 1,'app/static/decred_90.png')
    return render_template('decred.html', results = results.items())

@app.route('/index/ZCoin', methods=['GET', 'POST'])
@app.route('/index/ZCoin/', methods=['GET', 'POST'])
@app.route('/ZCoin', methods=['GET', 'POST'])
@app.route('/ZCoin/', methods=['GET', 'POST'])
def zcoin():
    results= get_prices(['XZC'],['ZCoin'])
    turn_prices_to_graph('XZC', 7, 1,'app/static/zcoin_7.png')
    turn_prices_to_graph('XZC', 30, 1,'app/static/zcoin_30.png')
    turn_prices_to_graph('XZC', 60, 1,'app/static/zcoin_60.png')
    turn_prices_to_graph('XZC', 90, 1,'app/static/zcoin_90.png')
    return render_template('zcoin.html', results = results.items())

@app.route('/index/Syscoin', methods=['GET', 'POST'])
@app.route('/index/Syscoin/', methods=['GET', 'POST'])
@app.route('/Syscoin', methods=['GET', 'POST'])
@app.route('/Syscoin/', methods=['GET', 'POST'])
def syscoin():
    results= get_prices(['SYS'],['Syscoin'])
    turn_prices_to_graph('SYS', 7, 1,'app/static/syscoin_7.png')
    turn_prices_to_graph('SYS', 30, 1,'app/static/syscoin_30.png')
    turn_prices_to_graph('SYS', 60, 1,'app/static/syscoin_60.png')
    turn_prices_to_graph('SYS', 90, 1,'app/static/syscoin_90.png')
    return render_template('syscoin.html', results = results.items())

@app.route('/index/MaidSafeCoin', methods=['GET', 'POST'])
@app.route('/index/MaidSafeCoin/', methods=['GET', 'POST'])
@app.route('/MaidSafeCoin', methods=['GET', 'POST'])
@app.route('/MaidSafeCoin/', methods=['GET', 'POST'])
def maidsafecoin():
    results= get_prices(['MAID'],['Steem'])
    turn_prices_to_graph('MAID', 7, 1,'app/static/maidsafecoin_7.png')
    turn_prices_to_graph('MAID', 30, 1,'app/static/maidsafecoin_30.png')
    turn_prices_to_graph('MAID', 60, 1,'app/static/maidsafecoin_60.png')
    turn_prices_to_graph('MAID', 90, 1,'app/static/maidsafecoin_90.png')
    return render_template('maidsafecoin.html', results = results.items())

@app.route('/index/LBRY Credits', methods=['GET', 'POST'])
@app.route('/index/LBRY Credits/', methods=['GET', 'POST'])
@app.route('/LBRY Credits', methods=['GET', 'POST'])
@app.route('/LBRY Credits/', methods=['GET', 'POST'])
def lbry_credits():
    results= get_prices(['LBC'],['LBRY Credits'])
    turn_prices_to_graph('LBC', 7, 1,'app/static/lbc_credits_7.png')
    turn_prices_to_graph('LBC', 30, 1,'app/static/lbc_credits_30.png')
    turn_prices_to_graph('LBC', 60, 1,'app/static/lbc_credits_60.png')
    turn_prices_to_graph('LBC', 90, 1,'app/static/lbc_credits_90.png')
    return render_template('lbry_credits.html', results = results.items())
    
@app.route('/index/OKCash', methods=['GET', 'POST'])
@app.route('/index/OKCash/', methods=['GET', 'POST'])
@app.route('/OKCash', methods=['GET', 'POST'])
@app.route('/OKCash/', methods=['GET', 'POST'])
def okcash():
    results= get_prices(['OK'],['OKCash'])
    turn_prices_to_graph('OK', 7, 1,'app/static/okcash_7.png')
    turn_prices_to_graph('OK', 30, 1,'app/static/okcash_30.png')
    turn_prices_to_graph('OK', 60, 1,'app/static/okcash_60.png')
    turn_prices_to_graph('OK', 90, 1,'app/static/okcash_90.png')
    return render_template('okcash.html', results = results.items())

@app.route('/index/Bancor Network', methods=['GET', 'POST'])
@app.route('/index/Bancor Network/', methods=['GET', 'POST'])
@app.route('/Bancor Network', methods=['GET', 'POST'])
@app.route('/Bancor Network/', methods=['GET', 'POST'])
def bancor_network_token():
    results= get_prices(['BNT'],['Bancor Network'])
    turn_prices_to_graph('BNT', 7, 1,'app/static/bancornetworktoken_7.png')
    turn_prices_to_graph('BNT', 30, 1,'app/static/bancornetworktoken_30.png')
    turn_prices_to_graph('BNT', 60, 1,'app/static/bancornetworktoken_60.png')
    turn_prices_to_graph('BNT', 90, 1,'app/static/bancornetworktoken_90.png')
    return render_template('bancornetworktoken.html', results = results.items())

@app.route('/search', methods=['GET', 'POST'])
def search():
    tickers = ['BTC', 'ETH', 'LTC', 'ETC', 'BCC', 'ZEC', 'XRP', 'NEO', 'DASH', 'IOTA', 'EOS', 'XCP', 'NEOS', 'XMR', 'LSK', 'GNT', 'WAVES', 'SNT', 'STRAT', 'VTC', 'XVG', 'DOGE', 'SC', 'ADA', 'SBD', 'BTS', 'GAS', 'REP', 'FCT', 'XLM', 'XEM', 'STEEM', 'PIVX', 'STORJ', 'DCR', 'XZC', 'SYS', 'MAID', 'LBC', 'OK', 'BNT']
    namesOfCurrency = ['Bitcoin', 'Ethereum', 'Litecoin', 'Ethereum Classic', 'Bitcoin Cash', 'Zcash' ,'Ripple', 'Neo', 'Dash', 'IOTA', 'EOS', 'Counterparty', 'Neoscoin', 'Monero', 'Lisk', 'Golem', 'Waves', 'Status','Stratis', 'Vertcoin', 'Verge', 'Dogecoin', 'Siacoin', 'Cardano', 'Steem Dollars', 'Bitshares', 'Gas', 'Augur', 'Factom', 'Stellar Lumens', 'Nem', 'Steem', 'Pivx', 'Storj', 'Decred', 'ZCoin', 'Syscoin', 'MaidSafeCoin', 'LBRY Credits', 'OKCash', 'Bancor Network']
    searchQuery = request.form['search']
    pattern = searchQuery.lower()
    pattern += '*'
    tickers_temp=[]
    namesOfCurrency_temp=[]
    resd={}
    for i in range(len(tickers)):
        tickers_temp.append(tickers[i].lower())
    for i in range(len(namesOfCurrency)):
        namesOfCurrency_temp.append(namesOfCurrency[i].lower())

    matching = fnmatch.filter(namesOfCurrency_temp, pattern)
    matching2 = fnmatch.filter(tickers_temp, pattern)
    for item in matching:
        index = namesOfCurrency_temp.index(item)
        resd[namesOfCurrency[index]]=tickers[index]
    return render_template("search_results.html", results= resd.items())


@app.route('/application', methods=['GET', 'POST'])
def application():
    d = collections.OrderedDict()
    fname = request.form['fname']
    lname = request.form['lname']
    resume = request.form['resume']
    linkedin = request.form['linkedin']
    email = request.form['email']
    phone = request.form['phone']
    d['First Name']=fname
    d['Last Name']=lname
    d['Resume']=resume
    d['Linkedin']=linkedin
    d['Email']=email
    d['Phone']=phone
    filename = codecs.open('app/static/'+ fname + '_' + lname + '.txt', 'w')
    print >> filename, d
    return redirect(url_for("careers"))



