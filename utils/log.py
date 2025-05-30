from datetime import datetime
import os

def log_trade_alert(ticker, data, market_sentiment, news_sentiment, rationale):
    log_entry = f"""
[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]
Ticker: {ticker}
Price: £{round(float(data['Close']), 2)}
RSI: {round(float(data['RSI']), 2)}
MA50: {round(float(data['MA50']), 2)}
Sentiment: {market_sentiment}, News: {news_sentiment}
Reason: {rationale}
---------------------------
"""
    os.makedirs("logs", exist_ok=True)
    with open("logs/trade_log.txt", "a") as f:
        f.write(log_entry)