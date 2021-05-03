"""
Plot S&P 500 ETF (VOO) trading strategies during 2020:
- Buy and Hold
- Dollar-Cost Averaging
- Simple Moving Average Crossover
"""

from fastquant.config import INIT_CASH
from fastquant import backtest, get_stock_data

voo = get_stock_data("VOO", "2020-01-01", "2021-01-01")

backtest('buynhold', voo)

# Approximate dollar-cost averaging over 1 year.
backtest('buynhold', voo, init_cash=1, add_cash_amount=90000)

backtest('smac', voo, fast_period=15, slow_period=40,
    # 3% commission naively approximates short-term capital gains tax, labor to trade, and risk-adjustment.
    commission=0.03)
