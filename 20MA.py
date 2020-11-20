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
BTC = 'BTCUSDT'
ETH = 'ETHUSDT'

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
        kline_BTC = GetKline(url, BTC, '1d')
        kline_ETH = GetKline(url, ETH, '1d')
        index_BTC = MA(kline_BTC, 20)
        index_ETH = MA(kline_ETH, 20)
        price_BTC = GetAvgPrice(url, BTC)
        price_ETH = GetAvgPrice(url, ETH)
        bias_BTC = (price_BTC - index_BTC[-1])/index_BTC[-1] * 100
        bias_ETH = (price_ETH - index_ETH[-1])/index_ETH[-1] * 100
        if price_BTC > index_BTC[-1]:
            msg = f'BTC 當前價格為: {int(price_BTC)}, 高於20日均線: {int(index_BTC[-1])} \n 🔥＊牛市看漲＊🔥 \n \n 均線乖離率：{int(bias_BTC)}%'
            Line(msg)
        else:
            msg = f'BTC 當前價格為: {int(price_BTC)}, 低於20日均線: {int(index_BTC[-1])} \n 🤮＊熊市看跌＊🤮 \n \n  均線乖離率：{int(bias_BTC)}%'
            Line(msg)
        if price_ETH > index_ETH[-1]:
            msg = f'ETH 當前價格為: {int(price_ETH)}, 高於20日均線: {int(index_ETH[-1])} \n 🔥＊牛市看漲＊🔥 \n \n  均線乖離率：{int(bias_ETH)}%'
            Line(msg)
        else:
            msg = f'ETH 當前價格為: {int(price_ETH)}, 低於20日均線: {int(index_ETH[-1])} \n 🤮＊熊市看跌＊🤮 \n \n 均線乖離率：{int(bias_ETH)}%'
            Line(msg)

        time.sleep(14400) # 4小時執行一次