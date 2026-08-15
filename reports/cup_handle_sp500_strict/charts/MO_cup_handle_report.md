# MO Cup-And-Handle Weekly Scan

Data source: yfinance weekly OHLCV, generated through 2026-05-25.
One-year chart: MO_weekly_cup_handle_1y.png
Pattern-context chart: MO_weekly_cup_handle_context.png

This is technical-pattern research, not investment advice.

## Summary

| Item | Read |
| --- | --- |
| Pattern bucket | Cup and Handle Pattern in Force |
| Verdict | Strong: Clean cup/handle geometry with stronger confirmation traits. |
| Score | 79.43/100 |
| Latest weekly close | 69.58 on 2026-05-25 |
| Breakout trigger | Weekly close above 74.56 (+7.2% from latest close) |
| Potential measured target | 87.79 (+26.2% from latest close, if breakout confirms) |
| Handle risk / invalidation area | Below handle low 64.08 (-7.9% from latest close) |
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
| 1st Pivot | 2025-10-06 | 67.12 | Left rim of the cup. |
| Cup | 2026-01-05 | 54.7 | Low point of the cup. |
| 2nd Pivot | 2026-04-06 | 67.93 | Right rim / resistance area. |
| Handle | 2026-04-13 | 64.08 | Handle pullback low. |
| Handle End | 2026-05-25 | 74.56 | Breakout level to watch. |
| Measured target | n/a | 87.79 | Breakout level plus cup depth. |

## Pattern Quality

| Check | Result | Read |
| --- | ---: | --- |
| Cup depth | 19.48% | Deep but still within the script's loose scan range. |
| Cup width | 26 weeks | Long enough to qualify as a weekly base candidate. |
| Handle width | 7 weeks | Short/current handle; still forming. |
| Handle depth | 29.1% of cup depth | Pullback is deeper than ideal, so confirmation matters. |
| Rim gap | 1.19% | Right rim is below the left rim; this weakens symmetry. |
| Ideal upper-half handle floor | 61.32 | Handle quality improves if it holds above this zone. |
| Volume | n/a | handle avg volume 0.99x cup avg; latest week 1.13x handle avg. |

## Interpretation

- TSLA currently fits the video-style scanner bucket `Cup and Handle Pattern in Force`.
- The bullish trigger is a weekly breakout above `74.56`.
- A simple measured target after confirmation is `87.79`.
- The setup weakens if price loses the handle low near `64.08`.
- Visible inside the one-year chart: yes.

## Caveats

- cup has a declining left side, rising right side, and rounded U-shape fit
- handle remains in upper half of the cup
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
| 1 | 79.43 | Cup and Handle Pattern in Force | 2025-10-06 -> 2026-01-05 -> 2026-04-06; handle low 2026-04-13 | 74.56 |
| 2 | 74.33 | Cup and Handle Pattern in Force | 2025-08-18 -> 2026-01-05 -> 2026-04-06; handle low 2026-04-13 | 74.56 |
