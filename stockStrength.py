import requests
from bs4 import BeautifulSoup
from sympy import per
import yfinance as yf
import pandas as pd
import numpy as np

stocks = ['AAPL', 'TSLA', 'QCOM', 'XOM', 'JNJ', 'MCD', 'NVDA', 'AMD', 'FB', 'NFLX', 'UNH', 'OXY', 'ABBV', 'PFE', 'F']
PFA = []
v = []
score = []
stockslist = []
industry = []
market_cap = []


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
        mkcp = ticker.info['marketCap']
        market_cap.append(round(mkcp/1000000000))
        strength_score = (0-percent_from_ATH + (vol/2))/2 + ((mkcp/1000000000000))
        strength_score = round(strength_score, 2)
        score.append(round(strength_score, 1))
        stockslist.append(stock)
        sector = ticker.info['sector']
        industry.append(sector)
        
        
    except:
        continue
    
data = {'Stock': stockslist,
        'Industry': industry,
        'Market Cap (B)': market_cap,
        'Percent From ATHs': PFA,
        'Volatility': v,
        'Strength Score': score}

df = pd.DataFrame(data)
df = df.sort_values(by='Strength Score', ascending=False)
df.reset_index(drop = True, inplace=True)
df.index = np.arange(1, len(df)+1)
print(df)

