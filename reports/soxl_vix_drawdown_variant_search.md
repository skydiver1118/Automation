# SOXL VIX Drawdown Variant Search

Base idea: buy SOXL after VIX closes above 35, execute next open. Variants add risk exits, still next-open execution.
IS/OOS split: IS before 2020-01-01, OOS from 2020-01-01 onward.

Selection: top rows are ranked by IS drawdown first, then IS Sharpe and IS return. OOS columns are validation only.

## Selected Variants

| selection_rank | variant | is_return_pct | is_max_drawdown_pct | is_sharpe | oos_return_pct | oos_max_drawdown_pct | oos_sharpe | oos_exposure_days_pct | trades |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | exit VIX<10; trail 35%; exit below SMA100 | 52.52 | -35.15 | 0.312 | 450.58 | -52.43 | 0.809 | 12.78 | 51 |
| 2 | exit VIX<20; trail 35%; exit below SMA100 | 52.52 | -35.15 | 0.312 | 708.9 | -52.43 | 0.965 | 11.97 | 51 |
| 3 | exit VIX<10; exit below SMA100 | 73.44 | -35.27 | 0.364 | 450.58 | -52.43 | 0.809 | 12.78 | 51 |
| 4 | exit VIX<10; exit below SMA100; max 126d | 73.44 | -35.27 | 0.364 | 356.13 | -52.43 | 0.752 | 11.22 | 52 |
| 5 | exit VIX<20; exit below SMA100 | 73.44 | -35.27 | 0.364 | 708.9 | -52.43 | 0.965 | 11.97 | 51 |
| 6 | exit VIX<20; exit below SMA100; max 126d | 73.44 | -35.27 | 0.364 | 570.14 | -52.43 | 0.911 | 10.41 | 52 |
| 7 | exit VIX<10; exit below SMA50 | 59.87 | -37.08 | 0.337 | 852.59 | -52.43 | 1.009 | 11.6 | 55 |
| 8 | exit VIX<20; exit below SMA50 | 59.87 | -37.08 | 0.337 | 1088.42 | -52.43 | 1.102 | 11.1 | 55 |
| 9 | exit VIX<10; trail 25%; exit below SMA100 | 43.87 | -38.43 | 0.294 | 414.77 | -52.43 | 0.796 | 10.54 | 53 |
| 10 | exit VIX<15; trail 25% | 200.64 | -43.43 | 0.522 | 361.67 | -68.85 | 0.695 | 15.84 | 17 |
| 11 | exit VIX<10; trail 25% | 108.89 | -43.43 | 0.39 | 241.67 | -68.85 | 0.616 | 16.52 | 17 |
| 12 | exit VIX<20; trail 25% | 41.01 | -43.43 | 0.265 | 808.06 | -68.85 | 0.888 | 14.46 | 17 |
| 13 | exit VIX<15; trail 35% | 135.72 | -47.21 | 0.433 | 1320.63 | -66.93 | 0.969 | 22.63 | 12 |
| 14 | exit VIX<15; trail 35%; max 126d | 135.72 | -47.21 | 0.433 | 1188.06 | -66.93 | 0.948 | 20.76 | 13 |
| 15 | exit VIX<10; trail 35% | 27.03 | -47.21 | 0.25 | 1049.92 | -66.93 | 0.901 | 28.68 | 12 |
| 16 | exit VIX<10; trail 35%; max 126d | 27.03 | -47.21 | 0.25 | 1213.65 | -66.93 | 0.943 | 24.81 | 13 |
| 17 | exit VIX<20; trail 35% | 10.57 | -47.21 | 0.182 | 1991.29 | -66.93 | 1.09 | 17.89 | 12 |
| 18 | exit VIX<20; trail 35%; max 126d | 10.57 | -47.21 | 0.182 | 1796.14 | -66.93 | 1.071 | 16.02 | 13 |
| 19 | exit VIX<15 | 793.68 | -50.06 | 0.755 | 785.64 | -90.46 | 0.829 | 56.55 | 8 |
| 20 | exit VIX<15; max 252d | 793.68 | -50.06 | 0.755 | 788.5 | -84.73 | 0.827 | 36.85 | 9 |

## Outputs

- All variants: `C:\Users\skydiver1118\Documents\New project\reports\soxl_vix_drawdown_variant_search_all.csv`
- Selected variants: `C:\Users\skydiver1118\Documents\New project\reports\soxl_vix_drawdown_variant_search_selected.csv`
- Best selected daily curve: `C:\Users\skydiver1118\Documents\New project\reports\soxl_vix_drawdown_variant_search_best_daily.csv`
- Best selected trades: `C:\Users\skydiver1118\Documents\New project\reports\soxl_vix_drawdown_variant_search_best_trades.csv`