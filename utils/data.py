import yfinance as yf
import pandas as pd

def get_stock_data(ticker, period="6mo", interval="1d"):
    df = yf.download(ticker, period=period, interval=interval)
    if df.empty:
        raise ValueError(f"No data returned for ticker {ticker}")
    df["VolumeAvg"] = df["Volume"].rolling(window=20).mean()
    return df
