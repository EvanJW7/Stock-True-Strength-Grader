import requests
from bs4 import BeautifulSoup
from sympy import per
import yfinance as yf
import pandas as pd
PFA = []
v = []
score = []
stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'FB', 'NVDA',  'V', 'JPM', 'UNH', 'BAC', 'WMT', 'HD', 'MA',
          'XOM', 'PFE', 'DIS', 'ADBE', 'CRM', 'QCOM', 'AMD', 'AVGO', 'LLY', 'NKE', 'TMO', 'CMCSA', 'ORCL',
         'COST', 'INTC', 'NFLX', 'PYPL', 'MRK', 'T', 'UPS', 'TXN', 'UNP', 'TMUS', 'CRWD', 'AMAT', 'SBUX',
         'ABNB', 'SNOW', 'NOW', 'LRCX', 'SNAP', 'DKNG']
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
        strength_score = 0-percent_from_ATH + (vol)
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
df
#Current date: 1/26/22.