"""
Plot S&P 500 ETF (VOO) trading strategies from 2011 through 2020:
- Buy and Hold
- Simple Moving Average Crossover

Proof of installation of FastQuant by Lorenzo Ampil:

        pip install fastquant

Adapted from:
https://towardsdatascience.com/backtest-your-trading-strategy-with-only-3-lines-of-python-3859b4a4ab44

Downgraded MatPlot Lib to 3.2.2.
https://stackoverflow.com/a/63974376/1417849
"""
from fastquant import backtest, get_stock_data
voo = get_stock_data("VOO", "2011-01-01", "2021-01-01")

backtest('buynhold', voo)

backtest('smac', voo, fast_period=15, slow_period=40,
    # 2% commission naively approximates short-term capital gains tax, labor to trade, and risk-adjustment.
    commission=0.02)
