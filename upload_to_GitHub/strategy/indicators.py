# strategy/indicators.py
import numpy as np
import pandas as pd
import talib


def add_MA(df, short_period=5, long_period=20):
    df['MA_short'] = talib.SMA(df['close'], timeperiod=short_period)
    df['MA_long'] = talib.SMA(df['close'], timeperiod=long_period)
    return df


def add_RSI(df, period=14):
    df['RSI'] = talib.RSI(df['close'], timeperiod=period)
    return df


def add_Bollinger_Bands(df, period=20, nbdev=2):
    upper, middle, lower = talib.BBANDS(df['close'], timeperiod=period, nbdevup=nbdev, nbdevdn=nbdev, matype=0)
    df['BB_upper'] = upper
    df['BB_middle'] = middle
    df['BB_lower'] = lower
    return df


def add_MACD(df, fastperiod=12, slowperiod=26, signalperiod=9):
    macd, signal, hist = talib.MACD(df['close'], fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
    df['MACD'] = macd
    df['MACD_signal'] = signal
    df['MACD_hist'] = hist
    return df
