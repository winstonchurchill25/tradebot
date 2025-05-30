import os
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

def place_order(ticker, qty=1, side="buy", type="market", time_in_force="gtc"):
    try:
        order = api.submit_order(
            symbol=ticker,
            qty=qty,
            side=side,
            type=type,
            time_in_force=time_in_force
        )
        print(f"📤 Order placed: {side.upper()} {qty} {ticker}")
    except Exception as e:
        print(f"⚠️ Order failed for {ticker}: {e}")
