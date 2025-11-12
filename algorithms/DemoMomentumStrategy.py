"""
Simple Momentum Trading Strategy Demo
Uses moving average crossover to generate buy/sell signals
"""

from AlgorithmImports import *

class DemoMomentumStrategy(QCAlgorithm):
    """
    Demo momentum strategy using SMA crossover
    - Buys when fast SMA crosses above slow SMA
    - Sells when fast SMA crosses below slow SMA
    """

    def Initialize(self):
        """Initialize algorithm parameters and data"""
        # Set backtest period
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2023, 12, 31)

        # Set starting cash
        self.SetCash(100000)

        # Add SPY (S&P 500 ETF) with daily resolution
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol

        # Create moving average indicators
        self.fast_sma = self.SMA(self.symbol, 20, Resolution.Daily)
        self.slow_sma = self.SMA(self.symbol, 50, Resolution.Daily)

        # Warm up period to initialize indicators
        self.SetWarmUp(50)

        self.Debug("DemoMomentumStrategy initialized")

    def OnData(self, data):
        """Execute trading logic on new data"""
        # Skip if we're still warming up or indicators aren't ready
        if self.IsWarmingUp or not self.fast_sma.IsReady or not self.slow_sma.IsReady:
            return

        # Skip if we don't have data for our symbol
        if not data.ContainsKey(self.symbol):
            return

        # Get current holdings
        holdings = self.Portfolio[self.symbol].Quantity

        # Trading logic: SMA Crossover
        if self.fast_sma.Current.Value > self.slow_sma.Current.Value:
            # Bullish signal - buy if not already invested
            if holdings <= 0:
                self.SetHoldings(self.symbol, 1.0)  # Invest 100% of portfolio
                self.Debug(f"BUY: Fast SMA ({self.fast_sma.Current.Value:.2f}) > Slow SMA ({self.slow_sma.Current.Value:.2f})")

        elif self.fast_sma.Current.Value < self.slow_sma.Current.Value:
            # Bearish signal - sell if currently invested
            if holdings > 0:
                self.Liquidate(self.symbol)
                self.Debug(f"SELL: Fast SMA ({self.fast_sma.Current.Value:.2f}) < Slow SMA ({self.slow_sma.Current.Value:.2f})")

    def OnEndOfAlgorithm(self):
        """Called at the end of the backtest"""
        self.Debug(f"Final Portfolio Value: ${self.Portfolio.TotalPortfolioValue:.2f}")
        self.Debug(f"Total Return: {((self.Portfolio.TotalPortfolioValue / self.StartingCash) - 1) * 100:.2f}%")
