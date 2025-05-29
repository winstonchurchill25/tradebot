# utils/data.py
# Fetch historical stock data using yfinance

import yfinance as yf
import pandas as pd

def get_stock_data(ticker: str, period: str = "3mo", interval: str = "1d") -> pd.DataFrame:
    """
    Downloads historical stock data from Yahoo Finance using yfinance.

    Args:
        ticker (str): The stock symbol (e.g. "PLTR").
        period (str): Time period (e.g. "3mo", "6mo", "1y").
        interval (str): Data frequency (e.g. "1d", "1h").

    Returns:
        pd.DataFrame: OHLCV data with datetime index.
    """
    # Fetch data from Yahoo Finance using yfinance
    df = yf.download(ticker, period=period, interval=interval, progress=False)

    if df.empty:
        raise ValueError(f"No data returned for ticker {ticker}")

    # Clean up any rows with missing values
    df.dropna(inplace=True)

    return df
