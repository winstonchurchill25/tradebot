# utils/backtest.py
# Simulates strategy over historical data and logs performance

from utils.data import get_stock_data
from utils.indicators import calculate_indicators
from utils.strategy import check_buy_conditions

from datetime import datetime
import pandas as pd


def run_backtest(ticker: str, period: str = "6m"):
    """
    Run a backtest for the given ticker over the specified period (e.g., "6m", "1y").
    """
    print(f"\n🔁 Running backtest for {ticker} over {period}...\n")

    df = get_stock_data(ticker, period=period)
    df = calculate_indicators(df)

    trades = []
    capital = 1000  # Assume starting with £1000
    position = 0
    entry_price = 0
    holding_days = 5  # Simple holding period per trade

    for i in range(len(df) - holding_days):
        window = df.iloc[:i+1]
        current_row = df.iloc[i]

        # Mock sentiment inputs (for now)
        market_sentiment = "bullish"
        news_sentiment = "positive"

        if check_buy_conditions(window, market_sentiment, news_sentiment):
            entry_date = current_row.name.strftime("%Y-%m-%d")
            entry_price = current_row['Close']
            exit_price = df.iloc[i + holding_days]['Close']
            pct_return = (exit_price - entry_price) / entry_price
            pnl = capital * pct_return

            trades.append({
                "entry_date": entry_date,
                "entry_price": round(entry_price, 2),
                "exit_price": round(exit_price, 2),
                "pnl": round(pnl, 2),
                "return_pct": round(pct_return * 100, 2)
            })

    # === Print summary ===
    total_pnl = sum([t["pnl"] for t in trades])
    final_balance = capital + total_pnl

    print(f"Total Trades: {len(trades)}")
    print(f"Total PnL: £{round(total_pnl, 2)}")
    print(f"Final Balance: £{round(final_balance, 2)}")
    print("\nTrade Log:")
    for t in trades:
        print(f"{t['entry_date']} | Buy: £{t['entry_price']} -> Sell: £{t['exit_price']} | Return: {t['return_pct']}% | PnL: £{t['pnl']}")

    if not trades:
        print("No trades matched the criteria in the backtest period.")
