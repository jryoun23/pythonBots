#the goal of this python bot is to analyze market data using the ccxt python package to retrieve data as well as possibly in the near future make buy and sell requests

import config
import ccxt
import ta
import pandas as pd

API_KEY = config.COINBASE_API_KEY
API_PASSWORD = config.COINBASE_API_PASSWORD
API_PASSPHRASE = config.COINBASE_API_PASSPHRASE

exchange = ccxt.coinbasepro()

bars = exchange.fetch_ohlcv('ETH/USD', timeframe='15m', limit = 10)

df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high','low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

print(df)

# here we are going to be computing an upper and lower band with the formulas as follows

#upperband = 
#lowerband = 