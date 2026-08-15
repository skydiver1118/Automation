# SOXL VIX ATR Exit Search

Rules: buy SOXL next open after VIX closes above 35. Sell next open after VIX closes below the configured threshold or after an ATR trailing-stop signal.
ATR stop: SOXL close <= highest close since entry - multiplier * ATR(window). Split: IS before 2020-01-01, OOS from 2020-01-01.

## Selected Variants

| selection_rank | variant | is_return_pct | is_max_drawdown_pct | is_sharpe | oos_return_pct | oos_max_drawdown_pct | oos_sharpe | oos_exposure_days_pct | trades |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | exit VIX<10; ATR21 trail 3x | 151.73 | -39.29 | 0.455 | 2071.09 | -62.84 | 1.079 | 22.76 | 12 |
| 2 | exit VIX<10; ATR14 trail 3x | 151.73 | -39.29 | 0.455 | 1871.75 | -62.84 | 1.046 | 24.44 | 12 |
| 3 | exit VIX<15; ATR14 trail 3x | 138.85 | -39.29 | 0.447 | 1920.93 | -62.84 | 1.082 | 18.58 | 12 |
| 4 | exit VIX<15; ATR21 trail 3x | 138.85 | -39.29 | 0.447 | 1920.93 | -62.84 | 1.082 | 18.58 | 12 |
| 5 | exit VIX<10; ATR10 trail 3x | 144.34 | -39.29 | 0.446 | 1585.17 | -62.84 | 1.004 | 24.63 | 12 |
| 6 | exit VIX<15; ATR10 trail 3x | 133.77 | -39.29 | 0.44 | 1749.84 | -62.84 | 1.057 | 18.7 | 12 |
| 7 | exit VIX<20; ATR14 trail 3x | 27.94 | -39.29 | 0.229 | 1674.85 | -62.84 | 1.065 | 14.84 | 12 |
| 8 | exit VIX<20; ATR21 trail 3x | 27.94 | -39.29 | 0.229 | 1674.85 | -62.84 | 1.065 | 14.84 | 12 |
| 9 | exit VIX<20; ATR10 trail 3x | 25.21 | -39.29 | 0.22 | 1524.6 | -62.84 | 1.038 | 14.96 | 12 |
| 10 | exit VIX<15; ATR14 trail 2x | 138.62 | -40.77 | 0.454 | 748.02 | -76.91 | 0.853 | 15.02 | 20 |
| 11 | exit VIX<10; ATR14 trail 2x | 95.33 | -40.77 | 0.381 | 527.6 | -76.91 | 0.774 | 15.71 | 20 |
| 12 | exit VIX<20; ATR14 trail 2x | 27.82 | -40.77 | 0.226 | 1138.75 | -76.91 | 0.96 | 13.53 | 20 |
| 13 | exit VIX<15; ATR10 trail 5x | 163.86 | -44.25 | 0.459 | 867.93 | -72.45 | 0.867 | 25.62 | 10 |
| 14 | exit VIX<15; ATR10 trail 5x; cooldown 21d | 163.86 | -44.25 | 0.459 | 683.22 | -72.45 | 0.829 | 24.31 | 10 |
| 15 | exit VIX<10; ATR10 trail 5x | 50.59 | -44.25 | 0.301 | 1154.81 | -72.45 | 0.904 | 40.09 | 10 |
| 16 | exit VIX<10; ATR10 trail 5x; cooldown 21d | 50.59 | -44.25 | 0.301 | 915.36 | -72.45 | 0.867 | 38.78 | 10 |
| 17 | exit VIX<20; ATR10 trail 5x | 23.76 | -44.25 | 0.227 | 1424.91 | -72.45 | 1.008 | 17.96 | 10 |
| 18 | exit VIX<20; ATR10 trail 5x; cooldown 21d | 23.76 | -44.25 | 0.227 | 1133.91 | -72.45 | 0.982 | 16.65 | 10 |
| 19 | exit VIX<15; ATR21 trail 2x | 36.0 | -46.04 | 0.251 | 1114.49 | -66.93 | 0.951 | 15.02 | 20 |
| 20 | exit VIX<10; ATR21 trail 2x | 21.88 | -46.04 | 0.212 | 798.81 | -66.93 | 0.868 | 15.71 | 20 |

## Outputs

- All variants: `C:\Users\skydiver1118\Documents\New project\reports\soxl_vix_atr_exit_search_all.csv`
- Selected variants: `C:\Users\skydiver1118\Documents\New project\reports\soxl_vix_atr_exit_search_selected.csv`
- Best selected daily curve: `C:\Users\skydiver1118\Documents\New project\reports\soxl_vix_atr_exit_search_best_daily.csv`
- Best selected trades: `C:\Users\skydiver1118\Documents\New project\reports\soxl_vix_atr_exit_search_best_trades.csv`