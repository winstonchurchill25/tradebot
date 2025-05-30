import argparse
import json
import os
from utils.strategy import check_buy_conditions
from utils.backtest import run_backtest
from utils.data import get_stock_data
from utils.indicators import calculate_indicators
from utils.live_sentiment import fetch_news_sentiment
from utils.alert import send_telegram_alert
from utils.log import log_trade_alert
from utils.trader import place_order  # <-- Added for placing orders
from utils.ticker_manager import load_tickers, add_ticker, remove_ticker  # <-- Re-added ticker management

from dotenv import load_dotenv  # <-- Load API keys
load_dotenv()

OPEN_TRADES_FILE = "logs/open_trades.json"
STOP_LOSS_THRESHOLD = 0.1  # 10%
TAKE_PROFIT_THRESHOLD = 0.15  # 15%

def save_open_trade(ticker, entry_price, stop_loss_price, take_profit_price):
    trades = {}
    if os.path.exists(OPEN_TRADES_FILE):
        with open(OPEN_TRADES_FILE, "r") as f:
            trades = json.load(f)
    trades[ticker] = {
        "entry_price": entry_price,
        "stop_loss": stop_loss_price,
        "take_profit": take_profit_price
    }
    with open(OPEN_TRADES_FILE, "w") as f:
        json.dump(trades, f)

def check_stop_loss():
    if not os.path.exists(OPEN_TRADES_FILE):
        return
    with open(OPEN_TRADES_FILE, "r") as f:
        trades = json.load(f)

    updated_trades = trades.copy()
    for ticker, trade_data in trades.items():
        entry_price = trade_data["entry_price"]
        stop_loss_price = trade_data["stop_loss"]
        take_profit_price = trade_data["take_profit"]

        df = get_stock_data(ticker)
        current_price = df.iloc[-1]['Close']

        if current_price <= stop_loss_price:
            send_telegram_alert(f"❌ STOP-LOSS TRIGGERED for {ticker}: Current price £{round(current_price,2)} below stop-loss of £{round(stop_loss_price,2)}")
            print(f"❌ STOP-LOSS TRIGGERED for {ticker}")
            del updated_trades[ticker]
        elif current_price >= take_profit_price:
            send_telegram_alert(f"✅ TAKE-PROFIT TRIGGERED for {ticker}: Current price £{round(current_price,2)} reached take-profit of £{round(take_profit_price,2)}")
            print(f"✅ TAKE-PROFIT TRIGGERED for {ticker}")
            del updated_trades[ticker]

    with open(OPEN_TRADES_FILE, "w") as f:
        json.dump(updated_trades, f)

def format_buy_signal(ticker, rsi, ma50, close_price, stop_loss_price, take_profit_price, date):
    return (
        f"🚨 BUY SIGNAL: {ticker}\n"
        f"📅 Date: {date}\n"
        f"💰 Entry: £{round(close_price, 2)} | 🛑 Stop Loss: £{stop_loss_price} | 🎯 Take Profit: £{take_profit_price}\n"
        f"📈 Indicators: RSI = {round(rsi, 2)}, MA50 = {round(ma50, 2)}"
    )

parser = argparse.ArgumentParser()
parser.add_argument("--backtest", type=str, help="Backtest duration (e.g. 6m, 1y)")
parser.add_argument("--add", type=str, help="Add a new ticker to watchlist")
parser.add_argument("--remove", type=str, help="Remove a ticker from watchlist")
parser.add_argument("--list", action="store_true", help="Show current watchlist")
parser.add_argument("--run_once", action="store_true", help="Run once in live mode")
parser.add_argument("--analyse", action="store_true", help="Analyse current data")
parser.add_argument("--alert", action="store_true", help="Trigger alert evaluation")
parser.add_argument("--log", action="store_true", help="Display previous alerts")
parser.add_argument("--monitor", action="store_true", help="Check active trades for stop-loss")
args = parser.parse_args()

if args.list:
    tickers = load_tickers()
    print("📈 Current Watchlist:")
    for i, ticker in enumerate(tickers, start=1):
        print(f"{i}. {ticker}")
    exit()

if args.add:
    add_ticker(args.add)
    exit()

if args.remove:
    remove_ticker(args.remove)
    exit()

tech_tickers = load_tickers()

if args.backtest:
    for ticker in tech_tickers:
        print(f"\n🔁 Running backtest for {ticker} over {args.backtest}...")
        run_backtest(ticker, args.backtest)

if args.run_once or args.analyse or args.alert:
    for ticker in tech_tickers:
        df = get_stock_data(ticker)
        df = calculate_indicators(df)
        sentiment = fetch_news_sentiment(ticker)

        print(f"\n🔍 {ticker} Sentiment: {sentiment}")

        if args.analyse:
            print(df.tail(1)[["Close", "RSI", "MA50", "Volume", "VolumeAvg"]])

        if args.run_once or args.alert:
            market_sentiment = sentiment.get("market", "neutral")
            news_sentiment = sentiment.get("news", "neutral")

            signal = check_buy_conditions(df, market_sentiment, news_sentiment)

            if signal:
                print(f"✅ BUY conditions met for {ticker}")
                close_price = float(df.iloc[-1]['Close'])
                stop_loss_price = round(close_price * (1 - STOP_LOSS_THRESHOLD), 2)
                take_profit_price = round(close_price * (1 + TAKE_PROFIT_THRESHOLD), 2)

                rsi = df.iloc[-1]['RSI']
                ma50 = df.iloc[-1]['MA50']
                alert_msg = format_buy_signal(
                    ticker, rsi, ma50, close_price, stop_loss_price, take_profit_price, df.index[-1].strftime('%Y-%m-%d')
                )

                if args.alert:
                    send_telegram_alert(alert_msg)

                place_order(ticker, qty=1, side="buy")  # 💥 LIVE order execution

                latest = df.iloc[-1].to_dict()
                log_trade_alert(ticker, latest, market_sentiment, news_sentiment, alert_msg)
                save_open_trade(ticker, close_price, stop_loss_price, take_profit_price)
            else:
                print(f"❌ Conditions not met for {ticker}")

if args.monitor:
    check_stop_loss()

if args.log:
    with open("logs/trade_log.txt", "r") as f:
        print(f.read())
