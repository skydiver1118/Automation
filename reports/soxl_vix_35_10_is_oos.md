# SOXL VIX 35/10 next-open

Rules:

- Instrument: SOXL.
- Signal source: S&P 500 VIX index close (`^VIX`).
- Buy when VIX closes above 35; execute at the next SOXL open.
- Sell when VIX closes below 10; execute at the next SOXL open.
- Stay in cash otherwise. No leverage beyond SOXL, no DCA, no costs/slippage.
- Same split as the SOXL/TQQQ research: IS before 2020-01-01, OOS from 2020-01-01 onward.

Data range: 2010-03-11 to 2026-05-20 from yfinance adjusted OHLC.
Latest state: target `SOXL`, latest VIX close `17.44`, pending next-open action ``.
Current open trade: entered 2018-02-06 at 8.1364; marked through 2026-05-20 at 173.2.

## IS/OOS Summary

| period | date_range | cumulative_return_pct | cagr_pct | max_drawdown_pct | sharpe | volatility_pct | exposure_days_pct | trades | wins | losses | win_rate_pct | average_trade_return_pct | benchmark_return_pct | benchmark_max_drawdown_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IS | 2010-03-11 to 2019-12-31 | 1619.12 | 33.65 | -72.61 | 0.768 | 68.48 | 90.73 | 2 | 2 | 0 | 100.0 | 1358.66 | 2851.84 | -72.61 |
| OOS | 2020-01-02 to 2026-05-20 | 819.19 | 41.59 | -90.46 | 0.875 | 111.3 | 100.0 | 0 | 0 | 0 |  |  | 819.19 | -90.46 |
| Full | 2010-03-11 to 2026-05-20 | 16687.47 | 37.22 | -90.46 | 0.803 | 87.88 | 94.38 | 2 | 2 | 0 | 100.0 | 1358.66 | 28725.15 | -90.46 |

## Trades

| entry_date | exit_date | symbol | exit_to | entry_price | exit_price | return_pct | outcome | holding_calendar_days | holding_trading_days |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2010-05-10 | 2017-05-09 | SOXL | CASH | 0.6186 | 4.8784 | 688.62 | win | 2556 | 1762 |
| 2018-02-06 | 2026-05-20 | SOXL | OPEN | 8.1364 | 173.2 | 2028.71 | win | 3025 | 2082 |

## Outputs

- Daily curve: `C:\Users\skydiver1118\Documents\New project\reports\soxl_vix_35_10_is_oos_daily.csv`
- Trades: `C:\Users\skydiver1118\Documents\New project\reports\soxl_vix_35_10_is_oos_trades.csv`
- Summary: `C:\Users\skydiver1118\Documents\New project\reports\soxl_vix_35_10_is_oos_summary.csv`
- Annual table: `C:\Users\skydiver1118\Documents\New project\reports\soxl_vix_35_10_is_oos_annual.csv`