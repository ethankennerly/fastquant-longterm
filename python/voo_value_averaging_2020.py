"""
Plot S&P 500 ETF (VOO) trading strategies during 2020:
- Value Averaging
"""

from fastquant.config import INIT_CASH
from fastquant import backtest, get_stock_data

import sys
sys.path.append('.')
import strategies.value_averaging

voo = get_stock_data("VOO", "2020-01-01", "2021-01-01")

backtest('value_averaging', voo)
