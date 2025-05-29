# utils/indicators.py
# Calculate technical indicators for trading strategy

import pandas as pd
import pandas_ta as ta

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds RSI, MA50, and Volume Average to the price data.

    Args:
        df (pd.DataFrame): DataFrame containing OHLCV data.

    Returns:
        pd.DataFrame: Modified DataFrame with new indicators added.
    """
    # Ensure we have a copy to avoid modifying original
    df = df.copy()

    # Calculate Relative Strength Index (RSI)
    df["RSI"] = ta.rsi(df["Close"], length=14)

    # Calculate 50-day Moving Average
    df["MA50"] = df["Close"].rolling(window=50).mean()

    # Calculate 5-day average volume
    df["VolumeAvg"] = df["Volume"].rolling(window=5).mean()

    # Drop rows with NaNs (due to rolling calculations)
    df.dropna(inplace=True)

    return df