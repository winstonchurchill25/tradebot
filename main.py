# pltr_cli_trading_bot/main.py
# Entry point for CLI-based trading agent
# Initial version monitors PLTR and sends alerts based on swing strategy

import argparse
from utils.data import get_stock_data
from utils.indicators import calculate_indicators
from utils.strategy import check_buy_conditions
from utils.alert import send_telegram_alert
from utils.backtest import run_backtest

def main():
    parser = argparse.ArgumentParser(description="CLI Trading Bot for PLTR")
    parser.add_argument("--run-once", action="store_true", help="Run a one-time signal check")
    parser.add_argument("--analyze", action="store_true", help="Print current indicator values")
    parser.add_argument("--alert", action="store_true", help="Send alert if conditions are met")
    parser.add_argument("--backtest", type=str, help="Backtest strategy (e.g., 6m, 1y)")
    parser.add_argument("--log", action="store_true", help="Display previous alerts")

    args = parser.parse_args()
    ticker = "PLTR"  # Stock monitored initially; extendable later

    if args.run_once or args.analyze or args.alert:
        # Fetch and calculate indicators
        df = get_stock_data(ticker)
        df = calculate_indicators(df)

        if args.analyze:
            print(df.tail(1)[["Close", "RSI", "MA50", "Volume", "VolumeAvg"]])

        if args.run_once or args.alert:
            # Simulated sentiment inputs for now
            market_sentiment = "bullish"
            news_sentiment = "positive"

            # Check for buy signal
            signal = check_buy_conditions(
                df,
                market_sentiment=market_sentiment,
                news_sentiment=news_sentiment
            )

            if signal:
                print("✅ BUY conditions met for", ticker)

                # Placeholder GPT rationale
                rationale = "Price is above MA50 with healthy RSI and bullish news driving volume surge."

                # Send alert
                if args.alert:
                    send_telegram_alert(f"🚨 BUY SIGNAL for {ticker}: {rationale}")

                # Log detailed trade signal
                latest = df.iloc[-1].to_dict()
                log_trade_alert(ticker, latest, market_sentiment, news_sentiment, rationale)
            else:
                print("❌ Conditions not met for", ticker)

    elif args.backtest:
        run_backtest(ticker, args.backtest)

    elif args.log:
        with open("logs/trade_log.txt", "r") as f:
            print(f.read())

if __name__ == "__main__":
    main()
