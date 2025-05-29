# utils/alert.py
# Sends Telegram alerts and logs alerts with sentiment and rationale

import requests
from datetime import datetime

# 🛠 Replace these with your actual Telegram bot credentials
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

def send_telegram_alert(message: str) -> None:
    """
    Sends a Telegram message using Bot API.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("⚠️ Failed to send Telegram message:", e)

def log_trade_alert(ticker: str, latest_candle: dict,
                    market_sentiment: str, news_sentiment: str,
                    rationale: str) -> None:
    """
    Logs alert with price, indicators, and sentiment.

    Args:
        ticker (str): The stock symbol.
        latest_candle (dict): Contains 'Close', 'RSI', 'MA50', 'Volume', 'VolumeAvg'.
        market_sentiment (str): Market-wide sentiment.
        news_sentiment (str): News-related sentiment.
        rationale (str): GPT-style summary (can be mocked for now).
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_entry = (
        f"[{timestamp}] BUY ALERT - {ticker}\n"
        f"Price: ${latest_candle['Close']:.2f} | RSI: {latest_candle['RSI']:.1f} | "
        f"MA50: ${latest_candle['MA50']:.2f} | Volume: {latest_candle['Volume'] / 1e6:.2f}M "
        f"(Avg: {latest_candle['VolumeAvg'] / 1e6:.2f}M)\n"
        f"Market sentiment: {market_sentiment}\n"
        f"News sentiment: {news_sentiment}\n"
        f"GPT Rationale: {rationale}\n"
        + "-" * 60 + "\n"
    )

    # Append log to file
    with open("logs/trade_log.txt", "a") as f:
        f.write(log_entry)