# # 200MA Alartor

import pandas as pd
import requests
import time

from talib    import abstract
from datetime import datetime

# # DataFrame Setting
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth',100)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# # Global Variables Setting
url  = 'https://api.binance.com/'
coin = 'BTCUSDT'
coin_2 = 'ETHUSDT'

# # Line Notify #尾數t
def Line(msg):   
    url = ('https://maker.ifttt.com/trigger/BTC20MA/with/key/nrt45vHOp-XTazeZs53G7wFVMlXyWl-pLxjxjivLtQt' +
          '?value1='+str(msg))
    r = requests.get(url)      
    if r.text[:5] == 'Congr':  
        print('成功推送 (' +str(msg)+') 至 Line')
    return r.text

# # Get Market Data
def GetKline(url, symbol, interval):
    try:
        data = requests.get(url + 'api/v3/klines', params={'symbol': symbol, 'interval': interval, 'limit': 1000}).json()
    except Exception as e:
        print ('Error! problem is {}'.format(e.args[0]))
    tmp  = []
    pair = []
    for base in data:
        tmp  = []
        for i in range(0,6):
            if i == 0:
                base[i] = datetime.fromtimestamp(base[i]/1000)
            tmp.append(base[i])
        pair.append(tmp)
    df = pd.DataFrame(pair, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df.date = pd.to_datetime(df.date)
    df.set_index("date", inplace=True)
    df = df.astype(float)
    return df

def GetETHKline(url, symbol, interval):
    try:
        data = requests.get(url + 'api/v3/klines', params={'symbol': symbol, 'interval': interval, 'limit': 1000}).json()
    except Exception as e:
        print ('Error! problem is {}'.format(e.args[0]))
    tmp  = []
    pair = []
    for base in data:
        tmp  = []
        for i in range(0,6):
            if i == 0:
                base[i] = datetime.fromtimestamp(base[i]/1000)
            tmp.append(base[i])
        pair.append(tmp)
    df = pd.DataFrame(pair, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df.date = pd.to_datetime(df.date)
    df.set_index("date", inplace=True)
    df = df.astype(float)
    return df

def GetAvgPrice(url, symbol):
    try:
        price = requests.get(url + 'api/v3/avgPrice', params={'symbol': symbol}).json()['price']
    except Exception as e:
        print ('Error! problem is {}'.format(e.args[0]))
    return float(price)

# # Financial indicators
def MA(df, period):
    return abstract.MA(df, timeperiod=period, matype=0)

if __name__ == "__main__":
    while True:
        kline = GetKline(url, coin, '1d')
        kline_2 = GetETHKline(url, coin_2, '1d')
        index = MA(kline, 20)
        index_2 = MA(kline_2, 20)
        price = GetAvgPrice(url, coin)
        price_2 = GetAvgPrice(url, coin_2)
        bias = (price - index[-1])/index[-1] * 100
        bias_2 = (price_2 - index_2[-1])/index_2[-1] * 100
        if price > index[-1]:
            msg = f'BTC 當前價格為: {price}, 高於20日均線: {index[-1]}, 🔥🔥🔥＊買入訊號＊,均線乖離率：{bias}%'
            Line(msg)
        else:
            msg = f'BTC 當前價格為: {price}, 低於20日均線: {index[-1]}, 🤮🤮🤮＊賣出訊號＊,均線乖離率：{bias}%'
            Line(msg)
        if price_2 > index_2[-1]:
            msg = f'ETH 當前價格為: {price_2}, 高於20日均線: {index_2[-1]}, 🔥🔥🔥＊買入訊號＊,均線乖離率：{bias_2}%'
            Line(msg)
        else:
            msg = f'ETH 當前價格為: {price_2}, 低於20日均線: {index_2[-1]}, 🤮🤮🤮＊賣出訊號＊,均線乖離率：{bias_2}%'
            Line(msg)

        time.sleep(14400) # 4小時執行一次