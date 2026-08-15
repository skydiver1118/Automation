# Codex SOXL Only: TrendSpider vs Local Backtest

| Metric | TrendSpider | Local Python/yfinance | Difference |
| --- | ---: | ---: | ---: |
| Period | 2010-03-11 to 2026-05-20 | 2010-03-11 to 2026-05-20 | n/a |
| Candles | 4073 | not stored in local summary | n/a |
| Net performance % | 49,269.50 | 48,461.10 | 808.40 |
| SOXL asset return % | 24,358.60 | 28,725.16 | -4,366.56 |
| Excess vs SOXL % | 24,910.90 | 19,735.94 | 5,174.96 |
| Max drawdown % | -65.50 | -66.18 | 0.68 |
| Positions | 78 | 77 | 1 |
| Win rate % | 45.00 | 41.56 | 3.44 |
| Average return % | 16.37 | not captured | n/a |
| Reward/risk | 4.15 | not captured | n/a |
| Beta vs asset | 0.49 | not captured | n/a |

## Notes

- Both tests use daily SOXL with SMA50 > SMA63 as the long state and a 10% close-based stop.
- TrendSpider produced one additional analyzed position and a modestly higher strategy return.
- The largest mismatch is SOXL buy-and-hold asset return, which points to data vendor/adjustment differences rather than a strategy logic change.
- Local result comes from `backtest_results/soxl_smh_variant_search_all.csv`; TrendSpider values were read from the visible Tabular Data panel after running `Codex SOXL Only`.
