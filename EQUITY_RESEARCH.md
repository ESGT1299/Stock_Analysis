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

## Validation November 27 2026

The original 3 tests passed. After hardening, 14 tests pass on Python 3.13.14,
NumPy 2.2.3 and pandas 2.2.3 with warnings treated as errors. Tests include
known baseline values, future perturbation, invalid dates/prices/parameters,
initial-cost compounding, aligned benchmark dates and a full offline CLI run.
CI installs only `requirements-test.txt`; live Yahoo downloads are not required.

Offline usage: supply `--csv adjusted_prices.csv --train-size 10 --cost-bps 10
--output results.csv` in addition to `--start` and exclusive `--end`. The CSV
must have `Date,MSFT,SPY` columns with unique increasing dates and positive,
finite adjusted prices. The full CSV is validated before filtering so bad rows
are not silently hidden. The downloader no longer drops missing values before
validation. Missing data must be investigated, not silently imputed.

### English explanation

Returns are Pt/Pt-1-1. The forecast for session t is the expanding average of
MSFT returns strictly before t. SPY and zero-return baselines use the same dates.
The binary long/cash position follows the sign of the prior-data forecast.
Turnover is abs(position_t-position_previous), including the opening purchase.
Net return is (1-fee_fraction)*(1+position*asset_return)-1, charging fees before
the period return. This aligns the arithmetic with the independent walk-forward lab.
Strict input validation prevents infinite prices, invalid training windows and
negative costs from producing plausible-looking outputs.

This baseline tests reproducible research plumbing, not deployable trading.
It lacks executable fills, final liquidation, spreads, taxes, survivorship controls,
fundamentals and a preregistered final holdout. Live provider/adjustment semantics
were not validated in this increment. Legacy BTC files remain unchanged.
Interview question: why shift the expanding mean? To prevent the return being
predicted from appearing in its own forecast.

### Explicación en español

Los retornos son Pt/Pt-1-1. El pronóstico de la sesión t es la media creciente
de los retornos de MSFT anteriores a t. SPY y el pronóstico cero utilizan las
mismas fechas. La posición invierte o permanece en efectivo según el signo del
pronóstico. La rotación es la variación absoluta de la posición e incluye la
compra inicial. El retorno neto es (1-comisión)*(1+posición*retorno)-1: la comisión
se cobra antes del retorno del período. Así coincide con el laboratorio walk-forward.
Las validaciones rechazan precios infinitos, ventanas inválidas y costos negativos.

El módulo demuestra un flujo de investigación reproducible, no una estrategia
lista para operar. Faltan precios de ejecución, liquidación final, spreads,
impuestos, controles de supervivencia, fundamentales y un holdout final fijado
de antemano. No se validaron el proveedor en vivo ni sus ajustes en este avance.
El análisis histórico de Bitcoin se conserva. Pregunta de entrevista: ¿por qué
desplazar la media creciente? Para evitar que el retorno objetivo forme parte
de su propio pronóstico.
