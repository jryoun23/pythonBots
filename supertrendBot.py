#Joseph Young
#5/06/21
# the goal of this python bot is to analyze market data using the ccxt python package to retrieve data as well as possibly in the near future make buy and sell requests
#this bot in particular is attempting to use a SUPERTREND trading strategy.
#I plan to learn more about this strategy as I read into it.
#This is a bot derived from the partTimeLarry Supertrend video series

import config
import ccxt
import ta
import pandas as pd
pd.set_option('display.max_rows', None)

API_KEY = config.COINBASE_API_KEY
API_PASSWORD = config.COINBASE_API_PASSWORD
API_PASSPHRASE = config.COINBASE_API_PASSPHRASE

exchange = ccxt.coinbasepro()

bars = exchange.fetch_ohlcv('BTC/USD', timeframe='1m', limit = 100)

df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high','low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')


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

# FinalLowerBand = if((Current.basicLowerband < Previous.FinalLowerband) && (Previous.close < Previous.FinalLowerBand))
#                   {Current.BasicLowerband}
#                  else
#                   {PreviousFinalLowerband}

#--------SUPERTREND-------------
# Supertrend = if (Current.close <= Current.FinalUpperband)
#               {Current.FinalUpperband}
#               else 
#               {Current.FinalLowerband}

# -------AVERAGE TRUE RANGE------------ This is used to calculate average volatility of an asset in a certain period
# TR = MAX[(HIGH - LOW), ABS(H - PreviousClose) , ABS(L - PreviousClose)]
# ATR = SUM(TR over a period)/periodlength 
# It truly is just the AVERAGE TRUE RANGE over a certain period.

#First things first, lets calculate the TRUE RANGE
#Re-learning syntax for craeting functions in python and MY GOD its so easy

def tr(df):         #Calculates TrueRange
    df['Cp'] = df['close'].shift(1)
    df['h-l'] = df['high'] - df['low']
    df['ABS(h-Cp)'] = abs(df['high'] - df['Cp'])
    df['ABS(l-Cp)'] = abs(df['low'] - df['Cp'])
    trueRange = df[['h-l', 'ABS(h-Cp)', 'ABS(l-Cp)']].max(axis = 1)
    return trueRange
#this part i am going to try on my own and make sure I have this python function creating thing down
#So i was origninally trying to use the mean function by itself, but then I saw that there was a 'rolling' method is made for periods of data so I feel silly now.
#This is my second time using pandas ever cut me some slack


def atr(df, period = 7):        #Calculates Average true range of the last x TR's
    df['TR'] = tr(df)
    average = df['TR'].rolling(period).mean()
    return average
    # df['ATR'] = average



# now we are going to get into calculating the upper and lowerbands
#basicUpperband = (High+Low)/2 + Multiplier*ATR
#basicLowerband = (High+Low)/2 + Multiplier*ATR

def upperAndLowerband(df, multiplier = 3, period = 7):
    df['ATR'] = atr(df, period)     #can change the period is well using period =
    df['UpperBand'] = (df['high'] + df['low'])/2 + (multiplier*df['ATR'])
    df['LowerBand'] = (df['high'] + df['low'])/2 - (multiplier*df['ATR'])
    df ['trendIndicator'] = True

    for row in range(1, len(df.index)):
        print(row)
        prev = row - 1

        #this is the trend indicator that will keep track of when and where the buy/sell signals are
        #we are usign the upper/ lower bound and the current closing row to determine if the trend flips
        #if the current row close is greater than the previous upperband, then we generate a buy signal because we are in an uptrend, 
        # if the current row has close that is lesser than the lowerband, then we generate a sell signal and entering a downtrend
        # the upperband and loweband indicators are only going going to change if there is a new greater low(upperband) or higher high (lowerband)/ which is the trend indicator) 
        #if the close is on the middle of the uptrend and downtrens, there is no change in the trend value, so it stays the same as whatever it was


        #this portion of the code does not correctly adjust the bands, it just acts as a flag on the indicator
        if df['close'][row] > df['UpperBand'][prev]:        #true = uptrend | false = downtrend
            df['trendIndicator'][row]= True
            #THIS IS A BUY SIGNAL
        elif df['close'][row] < df['LowerBand'][prev]:
            df['trendIndicator'][row] = False
            #THIS IS A SELL SIGNAL
        else:
            #THIS IS A DO NOTHING SIGNAL
            df['trendIndicator'][row] = df['trendIndicator'][prev]
            if not df['trendIndicator'][row] and df['UpperBand'][row] > df['UpperBand'][prev]:      #if youre in a downtrend, we want to find the minimum value, so if the new upperband is higher than the old upperband, we want to keep the old upperband
                df['UpperBand'][row] = df['UpperBand'][prev]
            elif df['trendIndicator'][row] and df['LowerBand'][row] < df['LowerBand'][prev]:        # if we are in an uptrend, we want to keep the highest value for the lowerband
                df['LowerBand'][row] = df['LowerBand'][prev]

    return df

print(upperAndLowerband(df))

# print(df)