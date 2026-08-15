# SOXL/TQQQ Local Rotation Strategy Search

Tested 25,776 always-invested SOXL/TQQQ variants from 2010-03-11 to 2026-05-20. Signals use prior-close data and daily adjusted yfinance prices. Results exclude commissions, slippage, taxes, borrow/friction, and are in-sample optimized.

Baseline hurdle: automated SOXL-only SMA50/SMA63 state with 10% stop returned 41,069.80% with -66.18% max drawdown over each variant's comparable period.

Variants beating the SOXL-only hurdle by total return: 12,987 of 25,776.

## Top 10 By Excess Vs SOXL-Only

| rank | family | variant | rebalance | actual_range | net_perf_pct | excess_vs_soxl_only_pct | max_drawdown_pct | positions | win_rate_pct | median_trade_days | soxl_return_pct | tqqq_return_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Relative momentum rotation | 63d return_minus_half_vol, skip 10d, chosen/alternate above SMA50, 5% hysteresis, switch on 10% stop | monthly | 2010-06-25 to 2026-05-20 | 775116.8 | 734047.0 | -79.24 | 124 | 54.03 | 7.0 | 33468.63 | 34842.88 |
| 2 | Relative momentum rotation | 84d return_minus_half_vol, chosen/alternate above SMA200, 2% hysteresis, switch on 10% stop | weekly | 2010-07-13 to 2026-05-20 | 683841.21 | 642771.41 | -78.99 | 128 | 47.66 | 7.5 | 30967.21 | 35142.37 |
| 3 | Relative momentum rotation | 84d return_minus_half_vol, 2% hysteresis, switch on 10% stop | weekly | 2010-07-13 to 2026-05-20 | 671798.62 | 630728.82 | -78.99 | 136 | 48.53 | 7.5 | 30967.21 | 35142.37 |
| 4 | Relative momentum rotation | 84d return_minus_half_vol, chosen/alternate above SMA100, 2% hysteresis, switch on 10% stop | weekly | 2010-07-13 to 2026-05-20 | 622076.12 | 581006.32 | -78.99 | 140 | 49.29 | 7.0 | 30967.21 | 35142.37 |
| 5 | Relative momentum rotation | 63d return_minus_half_vol, skip 10d, 5% hysteresis, switch on 10% stop | monthly | 2010-06-25 to 2026-05-20 | 601067.08 | 559997.28 | -79.24 | 126 | 53.17 | 8.0 | 33468.63 | 34842.88 |
| 6 | Relative momentum rotation | 63d return_minus_half_vol, skip 10d, chosen/alternate above SMA200, 5% hysteresis, switch on 10% stop | monthly | 2010-06-25 to 2026-05-20 | 552991.56 | 511921.76 | -79.24 | 124 | 52.42 | 7.5 | 33468.63 | 34842.88 |
| 7 | Relative momentum rotation | 84d return_minus_half_vol, chosen/alternate above SMA200, 2% hysteresis, switch on 10% stop | daily | 2010-07-13 to 2026-05-20 | 549572.48 | 508502.68 | -79.33 | 176 | 49.43 | 7.0 | 30967.21 | 35142.37 |
| 8 | Relative momentum rotation | 63d return_minus_half_vol, skip 10d, chosen/alternate above SMA50, 5% hysteresis | monthly | 2010-06-25 to 2026-05-20 | 545131.65 | 504061.85 | -83.73 | 42 | 76.19 | 90.0 | 33468.63 | 34842.88 |
| 9 | Relative momentum rotation | 63d return_minus_half_vol, skip 10d, chosen/alternate above SMA50, 5% hysteresis, switch on 20% stop | monthly | 2010-06-25 to 2026-05-20 | 543565.64 | 502495.84 | -84.82 | 74 | 59.46 | 52.0 | 33468.63 | 34842.88 |
| 10 | Relative momentum rotation | 84d return_minus_half_vol, chosen/alternate above SMA200, switch on 10% stop | weekly | 2010-07-13 to 2026-05-20 | 540540.6 | 499470.8 | -80.03 | 134 | 48.51 | 7.0 | 30967.21 | 35142.37 |

## Best Variant Per Family

| rank | family | variant | rebalance | net_perf_pct | excess_vs_soxl_only_pct | max_drawdown_pct | positions | sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Relative momentum rotation | 63d return_minus_half_vol, skip 10d, chosen/alternate above SMA50, 5% hysteresis, switch on 10% stop | monthly | 775116.8 | 734047.0 | -79.24 | 124 | 1.15 |
| 1988 | Momentum pullback rotation | 63d leader fallback, buy weaker 5d pullback, pullback asset above SMA100 and positive long momentum, switch on 10% stop | daily | 146015.34 | 104161.09 | -81.85 | 812 | 1.01 |
| 2666 | Multi-lookback vote rotation | Vote (21, 63, 126), chosen/alternate above SMA200, switch on 10% stop | daily | 125824.9 | 84755.1 | -84.21 | 362 | 0.99 |

## Files

- Full grid: `reports\soxl_tqqq_rotation_search_all.csv`
- Top 50: `reports\soxl_tqqq_rotation_search_best.csv`
- Best equity curve: `reports\soxl_tqqq_rotation_best_equity.csv`
- Best allocation history: `reports\soxl_tqqq_rotation_best_allocation.csv`
- Equity plot: `reports\soxl_tqqq_rotation_best_equity.png`

## Interpretation

The strongest in-sample candidates favor short-to-intermediate relative strength between SOXL and TQQQ, usually with a switch-on-stop overlay. That lets the strategy ride SOXL during semiconductor surges and move into TQQQ when the broader leveraged Nasdaq trend is stronger.

The top row is not automatically production-ready because this search deliberately tried many combinations. The practical next step is to pick a simple high-ranking variant and run walk-forward or year-by-year validation before using it in the daily signal automation.