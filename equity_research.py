"""Chronological equity research benchmark; no trading recommendation."""
import argparse
import numpy as np
import pandas as pd
from numbers import Integral, Real

def evaluate(prices, train_size=252, cost_bps=10):
    """Prices: aligned, positive adjusted closes, indexed by trading date."""
    if not isinstance(prices, pd.DataFrame) or prices.empty or prices.columns.has_duplicates or not {'MSFT', 'SPY'} <= set(prices.columns):
        raise ValueError('A nonempty DataFrame with unique MSFT and SPY columns is required')
    if not isinstance(prices.index, pd.DatetimeIndex) or prices.index.hasnans or not prices.index.is_unique or not prices.index.is_monotonic_increasing:
        raise ValueError("Dates must be unique and increasing")
    if isinstance(train_size, bool) or not isinstance(train_size, Integral) or train_size < 1:
        raise ValueError('train_size must be a positive integer')
    if isinstance(cost_bps, bool) or not isinstance(cost_bps, Real) or not np.isfinite(cost_bps) or not 0 <= cost_bps < 10000:
        raise ValueError('cost_bps must be finite and in [0, 10000)')
    prices = prices[['MSFT', 'SPY']].astype(float)
    if not np.isfinite(prices.to_numpy()).all() or (prices <= 0).any().any():
        raise ValueError("Adjusted prices must be positive and complete")
    r = prices.pct_change(fill_method=None).iloc[1:]
    if not np.isfinite(r.to_numpy()).all() or (r <= -1).any().any():
        raise ValueError('Computed returns must be finite and greater than -100%')
    if len(r) <= train_size:
        raise ValueError("Insufficient history")
    # Each prediction uses returns strictly before the target session.
    prediction = r["MSFT"].expanding(min_periods=train_size).mean().shift(1)
    out = pd.DataFrame({"actual": r["MSFT"], "benchmark": r["SPY"],
                        "historical_mean": prediction, "zero": 0.0}).dropna()
    # Illustrative signal formed using information at prior close;
    # close-to-close performance is not an executable fill simulation.
    out["position"] = (out["historical_mean"] > 0).astype(float)
    turnover = out["position"].diff().abs()
    turnover.iloc[0] = abs(out["position"].iloc[0])
    out['turnover'] = turnover
    out['cost_fraction'] = turnover * cost_bps / 10000
    # Charge fees before applying this period's return, matching the lab convention.
    out["strategy_net"] = (1 - out['cost_fraction']) * (1 + out["position"] * out["actual"]) - 1
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2015-01-01")
    parser.add_argument("--end", required=True, help="Exclusive end date")
    parser.add_argument('--csv', help='Offline adjusted-price CSV with Date, MSFT and SPY columns')
    parser.add_argument('--train-size', type=int, default=252)
    parser.add_argument('--cost-bps', type=float, default=10)
    parser.add_argument('--output', default='equity_results.csv')
    args = parser.parse_args()
    start, end = pd.Timestamp(args.start), pd.Timestamp(args.end)
    if pd.isna(start) or pd.isna(end) or start >= end:
        parser.error('start must precede the exclusive end date')
    if args.csv:
        prices = pd.read_csv(args.csv, index_col='Date', parse_dates=['Date'])
        # Validate the full input before date filtering can conceal invalid rows.
        evaluate(prices, train_size=args.train_size, cost_bps=args.cost_bps)
        prices = prices.loc[(prices.index >= start) & (prices.index < end)]
    else:
        import yfinance as yf
        prices = yf.download(["MSFT", "SPY"], start=args.start, end=args.end,
                             auto_adjust=True, progress=False)["Close"]
    result = evaluate(prices, train_size=args.train_size, cost_bps=args.cost_bps)
    for name in ("historical_mean", "zero"):
        print(name, "MAE", (result[name] - result.actual).abs().mean())
    for name in ("actual", "benchmark", "strategy_net"):
        print(name, "cumulative return", (1 + result[name]).prod() - 1)
    result.to_csv(args.output)

if __name__ == "__main__":
    main()
