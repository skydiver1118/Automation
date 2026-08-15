# S&P 500 Membership Validation for Strategy Buys

Strategy checked: S&P 500 Top1/Top2/Top3 monthly skip-momentum, 126 trading-day lookback, skip latest 21 trading days, open-to-open execution.
Period checked: 2020-01-01 through 2026-05-17.
Membership source: local cached current S&P 500 constituents table, using the `Date added` column.

| Top N | Buy events | Unique tickers | Pass | Violations | Unknown date |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 41 | 27 | 16 | 25 | 0 |
| 2 | 71 | 44 | 30 | 41 | 0 |
| 3 | 117 | 72 | 58 | 59 | 0 |

A violation means the simulated purchase date is earlier than the stock's S&P 500 `Date added` value.
This confirms index-membership lookahead bias whenever violations are present.

## Violation Ticker Summary

| Ticker | Security | S&P 500 Date Added | First Purchase | Buy Events | Top N Variants | Max Days Early |
| --- | --- | --- | --- | ---: | --- | ---: |
| BLDR | Builders FirstSource | 2023-12-18 | 2020-01-02 | 4 | 1, 2, 3 | 1446 |
| DXCM | Dexcom | 2020-05-12 | 2020-01-02 | 7 | 1, 2, 3 | 131 |
| PODD | Insulet Corporation | 2023-03-15 | 2020-01-02 | 2 | 2, 3 | 1168 |
| APO | Apollo Global Management | 2024-12-23 | 2020-02-03 | 1 | 3 | 1785 |
| TSLA | Tesla, Inc. | 2020-12-21 | 2020-02-03 | 13 | 1, 2, 3 | 322 |
| MRNA | Moderna | 2021-07-21 | 2020-04-01 | 11 | 1, 2, 3 | 476 |
| PCG | PG&E Corporation | 2022-10-03 | 2020-05-01 | 6 | 1, 2, 3 | 885 |
| CRWD | CrowdStrike | 2024-06-24 | 2020-07-01 | 4 | 1, 2, 3 | 1454 |
| DDOG | Datadog | 2025-07-09 | 2020-08-03 | 5 | 2, 3 | 1801 |
| EQT | EQT Corporation | 2022-10-03 | 2020-08-03 | 6 | 1, 2, 3 | 791 |
| CVNA | Carvana | 2025-12-22 | 2020-10-01 | 14 | 1, 2, 3 | 1908 |
| XYZ | Block, Inc. | 2025-07-23 | 2020-11-02 | 1 | 3 | 1724 |
| GNRC | Generac | 2021-03-22 | 2020-12-01 | 1 | 3 | 111 |
| WBD | Warner Bros. Discovery | 2022-04-11 | 2021-04-01 | 1 | 3 | 375 |
| TPL | Texas Pacific Land Corporation | 2024-11-26 | 2021-05-03 | 7 | 1, 2, 3 | 1303 |
| BX | Blackstone Inc. | 2023-09-18 | 2021-09-01 | 2 | 2, 3 | 747 |
| ON | ON Semiconductor | 2022-06-21 | 2022-01-03 | 1 | 3 | 169 |
| FSLR | First Solar | 2022-12-19 | 2022-10-03 | 4 | 1, 2, 3 | 77 |
| SMCI | Supermicro | 2024-03-18 | 2022-10-03 | 15 | 1, 2, 3 | 532 |
| ERIE | Erie Indemnity | 2024-09-23 | 2022-12-01 | 1 | 3 | 662 |
| AXON | Axon Enterprise | 2023-05-04 | 2023-01-03 | 4 | 1, 2, 3 | 121 |
| APP | AppLovin | 2025-09-22 | 2023-08-01 | 6 | 1, 2, 3 | 783 |
| PLTR | Palantir Technologies | 2024-09-23 | 2023-09-01 | 5 | 1, 2, 3 | 388 |
| VRT | Vertiv | 2026-03-23 | 2023-10-02 | 3 | 1, 2, 3 | 903 |
| DELL | Dell Technologies | 2024-09-23 | 2023-12-01 | 2 | 3 | 297 |
| COIN | Coinbase | 2025-05-19 | 2024-01-02 | 5 | 1, 2, 3 | 503 |
| HOOD | Robinhood Markets | 2025-09-22 | 2024-08-01 | 5 | 1, 2, 3 | 417 |
| FIX | Comfort Systems USA | 2025-12-22 | 2025-09-02 | 1 | 3 | 111 |
| SATS | EchoStar | 2026-03-23 | 2025-10-01 | 3 | 2, 3 | 173 |
| SNDK | Sandisk | 2025-11-28 | 2025-11-03 | 3 | 1, 2, 3 | 25 |
| LITE | Lumentum | 2026-03-23 | 2025-12-01 | 4 | 2, 3 | 112 |
| CIEN | Ciena | 2026-02-09 | 2026-01-02 | 1 | 3 | 38 |

## Output Files

- Buy-level validation CSV: `reports\sp500_membership_validation_top1_top2_top3_monthly_o2o_2020_2026ytd.csv`
- Ticker summary CSV: `reports\sp500_membership_validation_top1_top2_top3_monthly_o2o_2020_2026ytd_ticker_summary.csv`
- Violations-only CSV: `reports\sp500_membership_validation_top1_top2_top3_monthly_o2o_2020_2026ytd_violations.csv`
- Excel workbook: `reports\sp500_membership_validation_top1_top2_top3_monthly_o2o_2020_2026ytd.xlsx`

Important limitation: this check uses the current constituent table's `Date added` field. A full institutional-quality test still needs a point-in-time S&P 500 membership history, including removals and re-additions.
