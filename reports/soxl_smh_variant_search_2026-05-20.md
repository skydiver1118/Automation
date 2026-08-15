# SOXL And SMH Variant Search

Run date: May 20, 2026  
Script: `C:\Users\skydiver1118\Documents\New project\scripts\soxl_smh_variant_search.py`  
Data: Yahoo Finance via `yfinance`; adjusted prices; no commissions, slippage, spread, borrow cost, financing, or tax effects.  
Search size: 9,832 variants across SOXL, SMH, intraday VWAP, intraday ORB, daily moving-average trend, daily absolute momentum, daily RSI pullback, and SMH/SOXL relative-strength rotation.

Important caveat: this is an in-sample parameter search. Results that beat the asset return should be treated as candidates for walk-forward testing, not as live-ready strategies.

## Best Overall Findings

| Rank | Strategy family | Variant | Symbol / benchmark | Timeframe | Period tested | Strategy return | Asset return | Excess | Strategy max DD | Asset max DD | Trades | Win rate |
|---:|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | SMH/SOXL rotation | Choose stronger of SMH/SOXL by 3-month return if positive, else AGG | SMH/SOXL/AGG vs SMH | Daily signal, monthly rebalance | 2010-03-11 to 2026-05-20 | 56,123.57% | 4,807.43% | 51,316.14 pp | -67.82% | -45.30% | 61 | 60.66% |
| 2 | SMH/SOXL rotation | Choose stronger of SMH/SOXL by 3-month return if positive, else AGG | SMH/SOXL/AGG vs SOXL | Daily signal, monthly rebalance | 2010-03-11 to 2026-05-20 | 56,123.57% | 28,725.15% | 27,398.42 pp | -67.82% | -90.46% | 61 | 60.66% |
| 3 | SOXL moving-average trend | SMA50/SMA63 state, 10% stop | SOXL vs SOXL | Daily | 2010-03-11 to 2026-05-20 | 48,461.10% | 28,725.16% | 19,735.94 pp | -66.18% | -90.46% | 77 | 41.56% |
| 4 | SOXL moving-average trend | SMA50/SMA63 state, 20% stop | SOXL vs SOXL | Daily | 2010-03-11 to 2026-05-20 | 42,856.34% | 28,725.16% | 14,131.18 pp | -66.40% | -90.46% | 56 | 51.79% |
| 5 | SOXL moving-average trend | SMA5/SMA150 state, no stop | SOXL vs SOXL | Daily | 2010-03-11 to 2026-05-20 | 37,705.78% | 28,725.16% | 8,980.63 pp | -71.43% | -90.46% | 23 | 52.17% |

The strongest same-asset result is the SOXL daily `SMA50/SMA63 state, 10% stop` variant. It beat SOXL buy-and-hold and reduced max drawdown from -90.46% to -66.18%, though a -66% drawdown is still severe. The highest total-return result is the SMH/SOXL 3-month rotation, but that is a rotation system, not a standalone SOXL or SMH strategy.

## Best Standalone SOXL Variants

| Rank | Family | Variant | Timeframe | Period tested | Strategy return | SOXL return | Excess | Strategy max DD | SOXL max DD | Trades | Win rate |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | Moving-average trend | SMA50/SMA63 state, 10% stop | Daily | 2010-03-11 to 2026-05-20 | 48,461.10% | 28,725.16% | 19,735.94 pp | -66.18% | -90.46% | 77 | 41.56% |
| 2 | Moving-average trend | SMA50/SMA63 state, 20% stop | Daily | 2010-03-11 to 2026-05-20 | 42,856.34% | 28,725.16% | 14,131.18 pp | -66.40% | -90.46% | 56 | 51.79% |
| 3 | Moving-average trend | SMA5/SMA150 state, no stop | Daily | 2010-03-11 to 2026-05-20 | 37,705.78% | 28,725.16% | 8,980.63 pp | -71.43% | -90.46% | 23 | 52.17% |
| 4 | Moving-average trend | SMA5/SMA150 cross, no stop | Daily | 2010-03-11 to 2026-05-20 | 37,705.78% | 28,725.16% | 8,980.63 pp | -71.43% | -90.46% | 23 | 52.17% |
| 5 | Moving-average trend | SMA8/SMA150 state, 10% stop | Daily | 2010-03-11 to 2026-05-20 | 33,686.84% | 28,725.16% | 4,961.68 pp | -71.76% | -90.46% | 27 | 44.44% |

## Best Standalone SMH Variants

No standalone SMH variant beat SMH buy-and-hold over the full daily period. The best SMH variants reduced drawdown, but gave up total return.

| Rank | Family | Variant | Timeframe | Period tested | Strategy return | SMH return | Excess | Strategy max DD | SMH max DD | Trades | Win rate |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | Moving-average trend | SMA13/SMA200 state, 20% stop | Daily | 2010-03-11 to 2026-05-20 | 2,591.23% | 4,807.43% | -2,216.21 pp | -33.02% | -45.30% | 14 | 50.00% |
| 2 | Absolute momentum | 126-day positive return, no trend SMA, 20% stop | Daily | 2010-03-11 to 2026-05-20 | 1,688.00% | 4,807.43% | -3,119.43 pp | -37.44% | -45.30% | 63 | 38.10% |
| 3 | RSI pullback | RSI3 <= 20, above SMA200, exit above SMA5, 20% stop | Daily | 2010-03-11 to 2026-05-20 | 609.91% | 4,807.43% | -4,197.52 pp | -11.89% | -45.30% | 239 | 71.55% |
| 4 | VWAP intraday | Long-only pullback, after 3 bars, no target, 1% stop | 15-minute | 2026-02-25 to 2026-05-20 | 19.57% | 32.19% | -12.62 pp | -2.62% | -15.69% | 95 | 43.16% |
| 5 | ORB intraday | Long-only, 3-bar ORB, volume >= 2.0x SMA20, no target | 5-minute | 2026-02-25 to 2026-05-20 | 6.02% | 32.75% | -26.73 pp | -3.58% | -15.77% | 32 | 50.00% |

## Best Intraday Variants

| ETF | Family | Variant | Timeframe | Period tested | Strategy return | Asset return | Excess | Strategy max DD | Asset max DD | Trades | Win rate |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| SOXL | VWAP intraday | Long-only pullback, after 3 bars, no target, 1% stop | 15-minute | 2026-02-25 to 2026-05-20 | 86.74% | 140.69% | -53.95 pp | -13.19% | -44.97% | 79 | 40.51% |
| SOXL | ORB intraday | Long-only, 3-bar ORB, no volume filter, no target | 5-minute | 2026-02-25 to 2026-05-20 | 40.57% | 143.77% | -103.20 pp | -12.21% | -45.15% | 44 | 50.00% |
| SMH | VWAP intraday | Long-only pullback, after 3 bars, no target, 1% stop | 15-minute | 2026-02-25 to 2026-05-20 | 19.57% | 32.19% | -12.62 pp | -2.62% | -15.69% | 95 | 43.16% |
| SMH | ORB intraday | Long-only, 3-bar ORB, volume >= 2.0x SMA20, no target | 5-minute | 2026-02-25 to 2026-05-20 | 6.02% | 32.75% | -26.73 pp | -3.58% | -15.77% | 32 | 50.00% |

Intraday VWAP and ORB did not beat buy-and-hold over the available recent intraday windows, but they reduced drawdown materially. That may still be useful for risk control, but not for full-period return leadership in this run.

## Variant Coverage

| Category | Variants tested |
|---|---:|
| Moving-average trend | 2,000 |
| RSI pullback | 5,760 |
| Absolute momentum | 560 |
| VWAP intraday | 720 |
| ORB intraday | 768 |
| SMH/SOXL relative-strength rotation | 24 |
| Total | 9,832 |

## Output Files

- Script: `C:\Users\skydiver1118\Documents\New project\scripts\soxl_smh_variant_search.py`
- All variants CSV: `C:\Users\skydiver1118\Documents\New project\backtest_results\soxl_smh_variant_search_all.csv`
- Beating variants CSV: `C:\Users\skydiver1118\Documents\New project\backtest_results\soxl_smh_variant_search_beating_asset.csv`
- Best by symbol/family CSV: `C:\Users\skydiver1118\Documents\New project\backtest_results\soxl_smh_variant_search_best_by_family_symbol.csv`
- All variants JSON: `C:\Users\skydiver1118\Documents\New project\backtest_results\soxl_smh_variant_search_all.json`
