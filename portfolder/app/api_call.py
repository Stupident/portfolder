import yfinance as yf
import requests
import json
from datetime import datetime, timedelta
import openai
from .config import openai_key
openai.api_key = openai_key
from pycoingecko import CoinGeckoAPI

def get_cryptocurrency_price(token, date):
    cg = CoinGeckoAPI()
    if date:
        price = cg.get_coin_history_by_id(ids=token, vs_currencies='usd', 
                        start=datetime.strftime(date, '%Y-%m-%d'), end=datetime.strftime(date+timedelta(days=7), '%Y-%m-%d')).get('usd')
    else:
        price = cg.get_price(ids=token, vs_currencies='usd').get(token).get('usd')
    return(price)

def get_price(ticker, date=None):
    asset = yf.Ticker(ticker)
    if date:
        hist = asset.history(start=datetime.strftime(date, '%Y-%m-%d'), end=datetime.strftime(date+timedelta(days=7), '%Y-%m-%d'))
        price = hist.values[0][0]
    else:
        price = asset.info['ask']
    return round(price, 4)

def get_crypto_price(ticker, date=None):
    asset = yf.Ticker(ticker)
    if date:
        hist = asset.history(start=datetime.strftime(date, '%Y-%m-%d'), end=datetime.strftime(date+timedelta(days=7), '%Y-%m-%d'))
        price = hist.values[0][0]
    else:
        price = asset.info['previousClose']
    print(price)
    return round(price, 4)

def get_ai_recommendation(user, portfolio):
    assets = portfolio.assets_value()
    portfolio_value = portfolio.total_curr_value()
    request_assets = []
    for asset in assets.items():
        if asset[0]:
            percent = asset[1]/portfolio_value
            request_assets.append(f'{asset[0]} - {asset[1]}$ становить {percent}%')

    request_assets_list = '; '.join(request_assets)
    request_header = f'Привіт, я {user.username}, надай мені конкретні рекомендації щодо моїх інвестицій, \
                        ніби ти фінансовий консультант в інвестиційній фірмі, яка піклується про клієнтів та їх заробіток. '
    request_portfolio_info = f'На даний момент мій інвестиційний портфель { portfolio.name } має вартість { portfolio_value }$ \
                            при початкових вкладеннях { portfolio.total_value() }$, \
                            тобто P&L становить { portfolio.pnl() }$ ({{portfolio.pnl_percent()}}%). '
    request = request_header + request_portfolio_info + request_assets_list
    print(request)
    response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages=[{'role' : 'user', 'content' : request}])
    print(response)
    recomends = response.choices[0].message.content
    return recomends

