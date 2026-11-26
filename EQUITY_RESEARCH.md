# Microsoft equity research — baseline
This module introduces an equity-focused alternative to the legacy BTC analysis without removing historical work.

## Reproduce
Python 3.11+:
```bash
pip install -r requirements-equity.txt
python -m unittest test_equity_research
python equity_research.py --start 2015-01-01 --end 2026-01-01
```

The model estimates next-session simple returns using only preceding returns and compares MAE against zero. SPY adjusted closes provide a broad-market ETF proxy, not the exact S&P 500 index. An illustrative long/cash signal incurs 10 bps per position change. The close-to-close convention is not a realistic execution simulation. No profitability is claimed; fundamentals, realistic fills, fixed holdout dates and richer models remain future work. Yahoo Finance data availability and adjustment conventions must be verified. Results are educational.
