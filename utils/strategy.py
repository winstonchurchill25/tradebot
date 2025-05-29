# utils/strategy.py
# Apply trading logic to determine whether to send a buy alert

import pandas as pd

def check_buy_conditions(df: pd.DataFrame,
                         market_sentiment: str = "neutral",
                         news_sentiment: str = "neutral",
                         reddit_sentiment: str = "neutral") -> bool:
    """
    Checks whether buy conditions are met using technicals + sentiment inputs.

    Args:
        df (pd.DataFrame): DataFrame with price and indicator columns.
        market_sentiment (str): "bullish", "bearish", or "neutral".
        news_sentiment (str): "positive", "negative", or "neutral".
        reddit_sentiment (str): Reserved for future Reddit integration.

    Returns:
        bool: True if buy conditions are met.
    """
    latest = df.iloc[-1]

    try:
        price = latest["Close"]
        ma50 = latest["MA50"]
        rsi = latest["RSI"]
        volume = latest["Volume"]
        volume_avg = latest["VolumeAvg"]
    except KeyError as e:
        raise ValueError(f"Missing expected column in DataFrame: {e}")

    # === Core Strategy Conditions ===
    conditions = {
        "price_above_ma50": price > ma50,
        "rsi_in_range": 45 <= rsi <= 60,
        "volume_spike": volume > 1.3 * volume_avg,
        "market_sentiment": market_sentiment == "bullish",
        "news_sentiment": news_sentiment == "positive"
        # "reddit_sentiment" can be added later here
    }

    # Print breakdown for debugging
    print("📊 Condition Check:")
    for k, v in conditions.items():
        print(f" - {k}: {'✅' if v else '❌'}")

    return all(conditions.values())