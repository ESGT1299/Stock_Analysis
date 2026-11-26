"""Chronological equity research benchmark; no trading recommendation."""
import argparse
import numpy as np
import pandas as pd

def evaluate(prices, train_size=252, cost_bps=10):
    """Prices: aligned, positive adjusted closes, indexed by trading date."""
    if not prices.index.is_unique or not prices.index.is_monotonic_increasing:
        raise ValueError("Dates must be unique and increasing")
    if prices.isna().any().any() or (prices <= 0).any().any():
        raise ValueError("Adjusted prices must be positive and complete")
    r = prices.pct_change().dropna()
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
    out["strategy_net"] = out["position"] * out["actual"] - turnover * cost_bps / 10000
    return out

def main():
    import yfinance as yf
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2015-01-01")
    parser.add_argument("--end", required=True, help="Exclusive end date")
    args = parser.parse_args()
    prices = yf.download(["MSFT", "SPY"], start=args.start, end=args.end,
                         auto_adjust=True, progress=False)["Close"].dropna()
    result = evaluate(prices)
    for name in ("historical_mean", "zero"):
        print(name, "MAE", (result[name] - result.actual).abs().mean())
    for name in ("actual", "benchmark", "strategy_net"):
        print(name, "cumulative return", (1 + result[name]).prod() - 1)
    result.to_csv("equity_results.csv")

if __name__ == "__main__":
    main()
