import requests
from bs4 import BeautifulSoup
from sympy import per
import yfinance as yf
import pandas as pd
import numpy as np
from tqdm import tqdm, trange
import time 
from time import sleep

stocks = ['XENE', 'NEX', 'OXY', 'KR', 'XOM', 'WMT', 'JNJ', 'KO', 'GOOGL', 'MA', 'AAPL', 'DDOG', 'PBF', 'AMZN', 'TSLA',
         'PEP', 'MSFT', 'MCD', 'NVDA', 'GS', 'JPM', 'SQ', 'PLTR', 'ROKU', 'TDOC']

PFA, v, score, stockslist, industry, market_cap, short_float, price, beta, dividend = [], [], [], [], [], [], [], [], [], []

for stock in stocks:
    ticker = yf.Ticker(stock)
    
    #Current Price
    try:
        current_price = ticker.info['currentPrice']
    except:
        current_price = 0
        
    #52-Week High
    try:
        ATH = ticker.info['fiftyTwoWeekHigh']
    except:
        ATH = 1
    percent_from_52 = round((1 - current_price/ATH)*100, 2)
    
    if percent_from_52 == 100:
        PFA.append(0)
    else:
         PFA.append(str(percent_from_52) + '%')
    
    #Volatility
    url = f'https://www.alphaquery.com/stock/{stock}/volatility-option-statistics/180-day/historical-volatility'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    
    try:
        volatility = soup.findAll('div', class_ = "indicator-figure-inner")[0]
        vol = float(volatility.text)*100
        vol = round(vol, 2)
        if vol == 0:
            v.append("No data")
        else:
            v.append(str(round(vol, 1)) + '%')
    except:
        vol = "No Data"
        v.append(vol)
    
    #Market Cap
    try:
        mkcp = ticker.info['marketCap']
        market_cap.append(round(mkcp/1000000000))
    except:
        mkcp = 0
        market_cap.append("No data")
 
    #Industry
    try:
        industry.append(ticker.info['sector'])
    except:
        industry.append("No data")
    
    #Short Float
    try:
        shorts = ticker.info['shortPercentOfFloat']
        shorts = round(float(shorts*100), 2)
        shortss = str(shorts) + '%'
        short_float.append(shortss)
    except:
        shorts = 0
        short_float.append("No data")
    
    #Strength Score
    if vol == 0:
        score.append("N/A")
    else:
        strength_score = ((0-percent_from_52 + (vol/1.5))/2 + (shorts/5))/2
        score.append(round(strength_score, 1))
        
    stockslist.append(stock)    
    price.append('$' + str(round(current_price, 2)))
        
data = {'Stock': stockslist,
        'Industry': industry,
        'Current Price': price,
        'Market Cap (B)': market_cap,
        '% Float Short': short_float,
        '% From 52w High': PFA,
        'Volatility': v,
        'Strength Score': score}

df = pd.DataFrame(data)
df = df.sort_values(by='Strength Score', ascending=False)
df.reset_index(drop = True, inplace=True)
df.index = np.arange(1, len(df)+1)

print(df)
