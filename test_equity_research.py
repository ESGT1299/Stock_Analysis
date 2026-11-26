import unittest
import numpy as np
import pandas as pd
from equity_research import evaluate

class EquityTests(unittest.TestCase):
    def prices(self):
        dates = pd.bdate_range("2020-01-01", periods=40)
        return pd.DataFrame({"MSFT": 100*np.cumprod(1+np.linspace(-.01,.02,40)),
                             "SPY": 100*np.cumprod(np.repeat(1.001,40))}, index=dates)
    def test_no_future_leakage(self):
        p = self.prices()
        first = evaluate(p, train_size=10)
        p.iloc[-1,0] *= 2
        second = evaluate(p, train_size=10)
        pd.testing.assert_series_equal(first.historical_mean, second.historical_mean)
    def test_baseline(self):
        p = self.prices()
        out = evaluate(p, train_size=10)
        expected = p.MSFT.pct_change().iloc[1:11].mean()
        self.assertAlmostEqual(out.historical_mean.iloc[0], expected)
    def test_invalid_prices(self):
        p = self.prices()
        p.iloc[5,0] = 0
        with self.assertRaises(ValueError):
            evaluate(p, train_size=10)

if __name__ == "__main__":
    unittest.main()
