# utils/strategy.py

def check_buy_conditions(df_window, market_sentiment="neutral", news_sentiment="neutral"):
    """Checks if buy conditions are met based on latest row in window."""
    if df_window.empty or len(df_window) < 1:
        return False  # Not enough data

    latest = df_window.iloc[-1]

    price = latest["Close"].iloc[0]
    ma50 = float(latest["MA50"].iloc[0])
    rsi = float(latest["RSI"].iloc[0])
    volume = float(latest["Volume"].iloc[0])
    volume_avg = float(latest["VolumeAvg"].iloc[0])

    conditions = {
        "price_above_ma50": price > ma50,
        "rsi_below_70": rsi < 70,
        "rsi_above_30": rsi > 30,
        "volume_above_avg": volume > volume_avg,
        "bullish_market": market_sentiment == "bullish",
        "positive_news": news_sentiment == "positive"
    }

    return all(conditions.values())
