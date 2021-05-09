#the goal of this python bot is to analyze market data using the ccxt python package to retrieve data as well as possibly in the near future make buy and sell requests
#this bot in particular is attempting to use a SUPERTREND trading strategy.
#I plan to learn more about this strategy as I read into it.

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
# It is going to be split up into two different sections 

#---------BASIC------------

#basicUpperband = (High+Low)/2 + Multiplier*ATR
#basicLowerband = (High+Low)/2 + Multiplier*ATR

#---------FINAL------------

# FinalUpperBand = if((Current.basicUpperband < Previous.FinalUpperband) && (Previous.close < Previous.FinalLowerBand))
#                   {Current.BasicLowerband}
#                  else
#                   {PreviousFinalLowerband}

# FinalUpperBand = if((Current.basicUpperband < Previous.FinalUpperband) && (Previous.close < Previous.FinalLowerBand))
#                   {Current.BasicLowerband}
#                  else
#                   {PreviousFinalLowerband}