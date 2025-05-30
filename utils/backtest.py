from utils.data import get_stock_data
from utils.indicators import calculate_indicators
from utils.strategy import check_buy_conditions
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime


def run_backtest(ticker: str, period: str = "6m"):
    print(f"\n🔁 Running backtest for {ticker} over {period}...\n")

    df = get_stock_data(ticker, period=period)
    df = calculate_indicators(df)

    trades = []
    capital = 1000  # Starting capital per trade
    holding_days = 5
    stop_loss_pct = 0.10  # 10% stop-loss

    for i in range(len(df) - holding_days):
        window = df.iloc[:i + 1].copy()

        # Ensure indicators are ready
        if len(window) < 60 or window[["MA50", "RSI", "VolumeAvg"]].isnull().any().any():
            continue

        current_row = window.iloc[-1]
        entry_date = current_row.name.strftime("%Y-%m-%d")
        entry_price = current_row["Close"].iloc[0]
        stop_price = entry_price * (1 - stop_loss_pct)

        market_sentiment = "bullish"
        news_sentiment = "positive"

        if check_buy_conditions(window, market_sentiment, news_sentiment):
            future_prices = df["Close"].iloc[i + 1:i + 1 + holding_days].values.flatten()

            # Stop-loss logic
            stop_hit_flags = future_prices < stop_price
            if np.any(stop_hit_flags):
                stop_idx = np.argmax(stop_hit_flags)
                exit_price = float(future_prices[stop_idx])
                exited_early = True
            else:
                exit_price = float(future_prices[-1])
                exited_early = False

            pct_return = (exit_price - entry_price) / entry_price
            pnl = capital * pct_return
            rsi = round(current_row["RSI"].iloc[0], 2)
            ma50 = round(current_row["MA50"].iloc[0], 2)
            close = round(current_row["Close"].iloc[0], 2)

            rationale = (
                f"Buy triggered on {entry_date} because:\n"
                f"- Sentiment: {market_sentiment}, News: {news_sentiment}\n"
                f"- Indicators: RSI = {rsi}, MA50 = {ma50}, Close = £{close}\n"
                f"- {'Exited early via stop-loss' if exited_early else 'Held full duration'}"
            )

            trades.append({
                "entry_date": entry_date,
                "entry_price": round(entry_price, 2),
                "exit_price": round(exit_price, 2),
                "pnl": round(pnl, 2),
                "return_pct": round(pct_return * 100, 2),
                "rationale": rationale
            })

      # === Summary ===
    total_pnl = round(sum(t["pnl"] for t in trades), 2)
    final_balance = round(capital + total_pnl, 2)

    summary = []
    summary.append(f"📊 Summary for {ticker} ({period}):")
    summary.append(f"Total Trades: {len(trades)}")
    summary.append(f"Total PnL: £{total_pnl}")
    summary.append(f"Final Balance: £{final_balance}")
    summary.append("")

    if trades:
        for t in trades:
            summary.append(f"📅 {t['entry_date']} | BUY £{t['entry_price']} → SELL £{t['exit_price']} | Return: {t['return_pct']}%")
            summary.append(f"🧠 {t['rationale']}")
            summary.append("")
    else:
        summary.append("No trades matched the criteria in the backtest period.\n")

    output_dir = Path("logs/backtests")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{ticker}_{period}_backtest.txt"
    with open(output_path, "w") as f:
        f.write("\n".join(summary))

    # Also print to console
    print("\n".join(summary))
    print(f"📄 Summary saved to {output_path}")