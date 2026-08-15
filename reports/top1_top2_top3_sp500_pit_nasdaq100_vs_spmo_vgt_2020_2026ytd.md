# Top1/Top2/Top3 Monthly Skip-Momentum Comparison

Period: 2020-01-01 through 2026-05-17.
Execution: monthly signal after month-end close, trade at next trading day's open, hold open-to-open.
Ranking: 126 trading-day momentum, skipping the latest 21 trading days.
S&P 500 rule: skip stocks whose `Date added` is after the purchase date, then choose the next eligible ranked stock.
Nasdaq-100 note: the cached Nasdaq-100 constituent table has no add-date field, so Nasdaq-100 rows use current constituents only.

| Universe | Top N | Membership Filter | Return | Max DD | Trades | Buys | Skipped Future Members | Violations | SPMO | VGT | Excess vs SPMO | Excess vs VGT | Final Holdings |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| S&P 500 | 1 | Date added | 1464.21% | -53.85% | 87 | 44 | 109 | 0 | 264.77% | 280.61% | 1199.44% | 1183.61% | SNDK |
| S&P 500 | 2 | Date added | 599.82% | -49.12% | 176 | 89 | 173 | 0 | 264.77% | 280.61% | 335.05% | 319.22% | SNDK, LITE |
| S&P 500 | 3 | Date added | 528.43% | -46.23% | 261 | 132 | 222 | 0 | 264.77% | 280.61% | 263.66% | 247.82% | SNDK, LITE, WDC |
| Nasdaq-100 | 1 | Not available/current constituents | 3606.85% | -67.36% | 77 | 39 | 0 | N/A | 264.77% | 280.61% | 3342.08% | 3326.24% | SNDK |
| Nasdaq-100 | 2 | Not available/current constituents | 6982.73% | -52.79% | 138 | 70 | 0 | N/A | 264.77% | 280.61% | 6717.96% | 6702.13% | SNDK, WDC |
| Nasdaq-100 | 3 | Not available/current constituents | 13331.01% | -45.49% | 205 | 104 | 0 | N/A | 264.77% | 280.61% | 13066.24% | 13050.40% | SNDK, WDC, STX |

## Output Files

- Excel workbook: `reports\top1_top2_top3_sp500_pit_nasdaq100_vs_spmo_vgt_2020_2026ytd.xlsx`
- Summary CSV: `reports\top1_top2_top3_sp500_pit_nasdaq100_vs_spmo_vgt_2020_2026ytd.csv`
- Trades CSV: `reports\top1_top2_top3_sp500_pit_nasdaq100_vs_spmo_vgt_2020_2026ytd_trades.csv`
- Monthly decisions CSV: `reports\top1_top2_top3_sp500_pit_nasdaq100_vs_spmo_vgt_2020_2026ytd_monthly_decisions.csv`
- Equity curve CSV: `reports\top1_top2_top3_sp500_pit_nasdaq100_vs_spmo_vgt_2020_2026ytd_equity_curve.csv`
