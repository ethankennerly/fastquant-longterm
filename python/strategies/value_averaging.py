#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Import standard library
# Strategy module for custom indicators input to backtest
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

# Import modules
import backtrader as bt

# Import from package
from fastquant.strategies import base
from fastquant.strategies.base import BaseStrategy
from fastquant.strategies.mappings import STRATEGY_MAPPING

# Base sell prop 1 overrides sell prop in the strategy.
base.SELL_PROP = 0.1

# Reduce trades.
ROI_THRESHOLD = 0.02

class ValueAveragingStrategy(BaseStrategy):
    """
    Naive Daily Value Averaging Strategy
    https://en.wikipedia.org/wiki/Value_averaging
    Has a fixed proportion to invest.
    Compounds that value each day.
    """

    def buy_signal(self):
        excess_roi = self.calculate_excess_roi()
        if excess_roi >= -ROI_THRESHOLD:
            return False
        self.buy_prop = -excess_roi
        num_days = len(self) + 1
        print(num_days, "buy_prop", self.buy_prop)
        return True

    def sell_signal(self):
        """
        This selling does not account for capital gains tax.
        """
        excess_roi = self.calculate_excess_roi()
        if excess_roi <= ROI_THRESHOLD:
            return False
        keep_prop = 1.0 / (1.0 + excess_roi)
        self.sell_prop = 1.0 - keep_prop
        num_days = len(self) + 1
        print(num_days, "sell_prop", self.sell_prop)
        return True

    def calculate_excess_roi(self):
        roi = self.calculate_position_roi()
        target_roi = self.calculate_target_roi()
        excess_roi = roi - target_roi
        return excess_roi

    def calculate_roi(self):
        """
        Broker value includes current cash.
        Value averaging might mean just the value of the investments at risk.
        """
        roi = (self.broker.get_value() / self.init_cash) - 1.0
        return roi

    def calculate_position_roi(self):
        """
        Excludes current cash.
        """
        broker = self.broker
        position_roi = ((broker.get_value() - broker.cash) / self.init_cash) - 1.0
        return position_roi

    def calculate_target_roi(self):
        self.target_fraction = 0.75
        self.annual_value_rate = 1.12
        self.trading_days_per_year = 252
        self.daily_value_rate = self.annual_value_rate ** (1.0/self.trading_days_per_year)
        num_days = len(self) + 1
        target_roi = self.daily_value_rate ** num_days
        target_roi *= self.target_fraction
        target_roi -= 1
        return target_roi

STRATEGY_MAPPING["value_averaging"] = ValueAveragingStrategy
