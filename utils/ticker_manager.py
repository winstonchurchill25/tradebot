import json
import os

TICKER_FILE = "tickers.json"

def load_tickers():
    if not os.path.exists(TICKER_FILE):
        return []
    with open(TICKER_FILE, "r") as f:
        return json.load(f).get("tech", [])

def save_tickers(tickers):
    with open(TICKER_FILE, "w") as f:
        json.dump({"tech": sorted(set(tickers))}, f, indent=2)

def add_ticker(ticker):
    tickers = load_tickers()
    if ticker.upper() not in tickers:
        tickers.append(ticker.upper())
        save_tickers(tickers)
        print(f"✅ Added {ticker.upper()} to ticker list.")
    else:
        print(f"⚠️ {ticker.upper()} already exists in the list.")

def remove_ticker(ticker):
    tickers = load_tickers()
    if ticker.upper() in tickers:
        tickers.remove(ticker.upper())
        save_tickers(tickers)
        print(f"🗑️ Removed {ticker.upper()} from ticker list.")
    else:
        print(f"⚠️ {ticker.upper()} not found in the list.")