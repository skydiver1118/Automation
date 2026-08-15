# IEX Cup-And-Handle Weekly Scan

Data source: yfinance weekly OHLCV, generated through 2026-05-25.
One-year chart: IEX_weekly_cup_handle_1y.png
Pattern-context chart: IEX_weekly_cup_handle_context.png

This is technical-pattern research, not investment advice.

## Summary

| Item | Read |
| --- | --- |
| Pattern bucket | Cup and Handle Pattern in Force |
| Verdict | Strong: Clean cup/handle geometry with stronger confirmation traits. |
| Score | 77.69/100 |
| Latest weekly close | 210.83 on 2026-05-25 |
| Breakout trigger | Weekly close above 223.85 (+6.2% from latest close) |
| Potential measured target | 291.71 (+38.4% from latest close, if breakout confirms) |
| Handle risk / invalidation area | Below handle low 203.45 (-3.5% from latest close) |
| Current state | awaiting breakout; no confirmed weekly breakout yet |

## How To Read The Score

| Score band | Meaning |
| --- | --- |
| 75-100 | Strong: clean geometry and stronger confirmation traits. |
| 60-74 | Good watchlist: pattern is usable but still needs confirmation. |
| 45-59 | Speculative watchlist: recognizable shape, but quality issues remain. |
| Below 45 | Weak: too many geometry/confirmation problems. |

This score is a pattern-quality score, not a probability forecast. It rewards cup symmetry, reasonable depth, rim alignment, handle quality, proximity to breakout, and healthier volume behavior.

## Key Levels

| Level | Date | Price | Meaning |
| --- | --- | ---: | --- |
| 1st Pivot | 2025-01-27 | 226.05 | Left rim of the cup. |
| Cup | 2025-09-22 | 158.19 | Low point of the cup. |
| 2nd Pivot | 2026-04-27 | 223.85 | Right rim / resistance area. |
| Handle | 2026-04-27 | 203.45 | Handle pullback low. |
| Handle End | 2026-05-25 | 223.85 | Breakout level to watch. |
| Measured target | n/a | 291.71 | Breakout level plus cup depth. |

## Pattern Quality

| Check | Result | Read |
| --- | ---: | --- |
| Cup depth | 30.02% | Deep but still within the script's loose scan range. |
| Cup width | 65 weeks | Long enough to qualify as a weekly base candidate. |
| Handle width | 4 weeks | Short/current handle; still forming. |
| Handle depth | 30.06% of cup depth | Pullback is deeper than ideal, so confirmation matters. |
| Rim gap | 0.97% | Right rim is below the left rim; this weakens symmetry. |
| Ideal upper-half handle floor | 192.12 | Handle quality improves if it holds above this zone. |
| Volume | n/a | handle avg volume 1.05x cup avg; latest week 1.06x handle avg. |

## Interpretation

- IEX currently fits the video-style scanner bucket `Cup and Handle Pattern in Force`.
- The bullish trigger is a weekly breakout above `223.85`.
- A simple measured target after confirmation is `291.71`.
- The setup weakens if price loses the handle low near `203.45`.
- Visible inside the one-year chart: partial only.

## Caveats

- cup has a declining left side, rising right side, and rounded U-shape fit
- handle remains in upper half of the cup
- right rim is modestly below the left rim
- no weekly close above the handle/rim resistance yet

## TrendSpider / Video Mapping

- The transcript workflow is: enable chart-pattern recognition, choose settings, scan a universe, optionally schedule the scan, then rank candidates by fundamentals/news/catalysts/technicals.
- Pattern in Force means a formed/active pattern waiting to break out.
- Breakout means price has moved through handle resistance.
- This script maps: left rim = 1st Pivot, bottom = Cup, right rim = 2nd Pivot, handle low/current handle = Handle, breakout level = Handle End.
- The chart adds Fibonacci-style reference lines and a shaded handle range, matching the video/article settings.

## Top Iterations

| Rank | Score | Bucket | Structure | Breakout |
| ---: | ---: | --- | --- | ---: |
| 1 | 77.69 | Cup and Handle Pattern in Force | 2025-01-27 -> 2025-09-22 -> 2026-04-27; handle low 2026-04-27 | 223.85 |
| 2 | 75.94 | Cup and Handle Pattern in Force | 2025-01-27 -> 2025-08-11 -> 2026-04-27; handle low 2026-04-27 | 223.85 |
| 3 | 74.87 | Cup and Handle Pattern in Force | 2025-01-27 -> 2025-10-13 -> 2026-04-27; handle low 2026-04-27 | 223.85 |
