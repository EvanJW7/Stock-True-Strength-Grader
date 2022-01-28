import requests
from bs4 import BeautifulSoup
from sympy import per
import yfinance as yf
import pandas as pd
import numpy as np

PFA = []
v = []
score = []
stocks = ['AAPL', 'MSFT', 'TSLA', 'XOM', 'ABBV', 'CVX', 'QCOM', 'PFE', 'ROKU', 'ZM', 'AMZN', 'UPS', 
          'NVDA', 'BAC', 'JPM', 'HOOD', 'SQ', 'HD', 'KR', 'WMT']
stockslist = []

for stock in stocks:
    try:
        ticker = yf.Ticker(stock)
        current_price = ticker.info['currentPrice']
        ATH = ticker.info['fiftyTwoWeekHigh']
        percent_from_ATH = round((1 - current_price/ATH)*100, 2)
        PFA.append(percent_from_ATH)
        url = f'https://www.alphaquery.com/stock/{stock}/volatility-option-statistics/180-day/historical-volatility'
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        volatility = soup.findAll('div', class_ = "indicator-figure-inner")[0]
        vol = float(volatility.text)*100
        vol = round(vol, 2)
        v.append(vol)
        strength_score = 0-percent_from_ATH + (vol/2)
        strength_score = round(strength_score, 2)
        score.append(strength_score)
        stockslist.append(stock)
    except:
        continue
    
data = {'Stock': stockslist,
        'Percent From ATHs': PFA,
        'Volatility': v,
        'Strength Score': score}

df = pd.DataFrame(data)
df = df.sort_values(by='Strength Score', ascending=False)
df.reset_index(drop = True, inplace=True)
df.index = np.arange(1, len(df)+1)
print(df)
#Current date: 1/28/22