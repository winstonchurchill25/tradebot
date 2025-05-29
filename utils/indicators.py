# utils/indicators.py
# Calculate technical indicators for trading strategy

import pandas as pd

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Calculate RSI (14-period)
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # 50-day moving average
    df["MA50"] = df["Close"].rolling(window=50).mean()

    # 5-day average volume
    df["VolumeAvg"] = df["Volume"].rolling(window=5).mean()

    df.dropna(inplace=True)
    return df
