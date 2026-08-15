# SOXL/TQQQ DCA Overlay Search

Tested 5,376 DCA overlay variants on the existing best SOXL/TQQQ rotation from 2010-06-25 to 2026-05-20. The core position remains 1 unit. DCA variants can add up to 2 extra units and sell extras on rebounds while keeping the 1-unit core.

Two account modes were tested: `reserve_cash` treats 3 units as full deployable account capital, so the core position is one-third invested; `margin_3x` keeps the original 1x core and allows exposure to rise as high as 3x.

## Best Drawdown Reducer

| rank_drawdown_first | variant | account_mode | anchor_mode | add1_drop_pct | add2_drop_pct | sell_mode | sell_param_pct | max_extra_days | net_return_pct | cagr_pct | max_drawdown_pct | sharpe | dca_trade_events | rotation_resets | max_units | extra_exposure_days_pct | base_rotation_return_pct | base_rotation_max_drawdown_pct | soxl_only_return_pct | soxl_only_max_drawdown_pct | beats_base_return | reduces_base_drawdown | reduces_soxl_only_drawdown |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | reserve_cash; anchor=entry; add at 15%/20%; sell=rebound_from_low 5%; max_extra_days=none | reserve_cash | entry | 15.0 | 20.0 | rebound_from_low | 5.0 | none | 5377.22 | 28.63 | -28.74 | 1.17 | 23 | 123 | 3 | 0.57 | 775116.8 | -79.24 | 41069.8 | -66.18 | False | True | True |

## Best Return Variant

| rank_return_first | rank_drawdown_first | variant | account_mode | anchor_mode | add1_drop_pct | add2_drop_pct | sell_mode | sell_param_pct | max_extra_days | net_return_pct | cagr_pct | max_drawdown_pct | sharpe | dca_trade_events | rotation_resets | max_units | extra_exposure_days_pct | base_rotation_return_pct | base_rotation_max_drawdown_pct | soxl_only_return_pct | soxl_only_max_drawdown_pct | beats_base_return | reduces_base_drawdown | reduces_soxl_only_drawdown |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 4661 | margin_3x; anchor=rolling_high; add at 5%/40%; sell=extra_profit 20%; max_extra_days=none | margin_3x | rolling_high | 5.0 | 40.0 | extra_profit | 20.0 | none | 6213084.81 | 100.19 | -97.29 | 1.2 | 208 | 123 | 3 | 71.15 | 775116.8 | -79.24 | 41069.8 | -66.18 | True | False | False |

## Key Finding

- Variants that reduced drawdown versus the base rotation: 3,390 of 5,376.
- Variants that reduced drawdown versus SOXL-only: 2,397 of 5,376.
- Margin-style DCA generally increases drawdown because it adds exposure into falling leveraged ETFs.
- Reserve-cash DCA reduces account drawdown, but total return is much lower because the normal core is only one-third invested.

## Files

- Full grid: `C:\Users\skydiver1118\Documents\New project\reports\soxl_tqqq_dca_overlay_search_all.csv`
- Best drawdown rows: `C:\Users\skydiver1118\Documents\New project\reports\soxl_tqqq_dca_overlay_best_drawdown.csv`
- Best return rows: `C:\Users\skydiver1118\Documents\New project\reports\soxl_tqqq_dca_overlay_best_return.csv`
- Curves: `C:\Users\skydiver1118\Documents\New project\reports\soxl_tqqq_dca_overlay_curves.csv`
- Unit exposure history: `C:\Users\skydiver1118\Documents\New project\reports\soxl_tqqq_dca_overlay_units.csv`
- Chart: `C:\Users\skydiver1118\Documents\New project\reports\soxl_tqqq_dca_overlay_curves.png`