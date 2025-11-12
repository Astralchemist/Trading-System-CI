"""
Simple Buy and Hold Strategy Demo
Buys SPY on day 1 and holds until the end
"""

from AlgorithmImports import *

class SimpleBuyAndHold(QCAlgorithm):
    """
    The simplest possible strategy - buy and hold SPY
    """

    def Initialize(self):
        """Initialize algorithm parameters"""
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2023, 12, 31)
        self.SetCash(100000)

        # Add SPY
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol

        self.Debug("SimpleBuyAndHold initialized - will buy on first day")

    def OnData(self, data):
        """Buy once and hold"""
        # Only buy if we don't have any holdings yet
        if not self.Portfolio.Invested:
            self.SetHoldings(self.symbol, 1.0)
            self.Debug(f"Bought SPY at ${data[self.symbol].Close:.2f}")

    def OnEndOfAlgorithm(self):
        """Report final results"""
        self.Debug(f"Final Portfolio Value: ${self.Portfolio.TotalPortfolioValue:.2f}")
        total_return = ((self.Portfolio.TotalPortfolioValue / self.StartingCash) - 1) * 100
        self.Debug(f"Buy and Hold Return: {total_return:.2f}%")
