# utils/broker.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = "https://paper-api.alpaca.markets"

def place_order(symbol, qty, side, type="market", time_in_force="gtc"):
    url = f"{ALPACA_BASE_URL}/v2/orders"
    headers = {
        "APCA-API-KEY-ID": ALPACA_API_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
    }
    order = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }
    response = requests.post(url, json=order, headers=headers)
    if response.status_code != 200:
        print(f"[ERROR] Order failed: {response.text}")
    else:
        print(f"[BROKER] Order placed: {side.upper()} {qty}x {symbol}")