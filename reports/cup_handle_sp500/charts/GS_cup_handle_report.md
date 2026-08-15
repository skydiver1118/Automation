# GS Cup-And-Handle Weekly Scan

Data source: yfinance weekly OHLCV, generated through 2026-05-25.
One-year chart: GS_weekly_cup_handle_1y.png
Pattern-context chart: GS_weekly_cup_handle_context.png

This is technical-pattern research, not investment advice.

## Summary

| Item | Read |
| --- | --- |
| Pattern bucket | Cup and Handle Pattern in Force |
| Verdict | Strong: Clean cup/handle geometry with stronger confirmation traits. |
| Score | 75.04/100 |
| Latest weekly close | 1025.56 on 2026-05-25 |
| Breakout trigger | Weekly close above 1027.22 (+0.2% from latest close) |
| Potential measured target | 1231.42 (+20.1% from latest close, if breakout confirms) |
| Handle risk / invalidation area | Below handle low 899.0 (-12.3% from latest close) |
| Current state | near breakout; no confirmed weekly breakout yet |

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
| 1st Pivot | 2026-01-12 | 984.7 | Left rim of the cup. |
| Cup | 2026-03-09 | 780.5 | Low point of the cup. |
| 2nd Pivot | 2026-04-20 | 952.01 | Right rim / resistance area. |
| Handle | 2026-05-04 | 899.0 | Handle pullback low. |
| Handle End | 2026-05-25 | 1027.22 | Breakout level to watch. |
| Measured target | n/a | 1231.42 | Breakout level plus cup depth. |

## Pattern Quality

| Check | Result | Read |
| --- | ---: | --- |
| Cup depth | 20.74% | Deep but still within the script's loose scan range. |
| Cup width | 14 weeks | Long enough to qualify as a weekly base candidate. |
| Handle width | 5 weeks | Short/current handle; still forming. |
| Handle depth | 25.96% of cup depth | Pullback is deeper than ideal, so confirmation matters. |
| Rim gap | 3.32% | Right rim is below the left rim; this weakens symmetry. |
| Ideal upper-half handle floor | 882.60 | Handle quality improves if it holds above this zone. |
| Volume | n/a | handle avg volume 0.82x cup avg; latest week 1.08x handle avg. |

## Interpretation

- TSLA currently fits the video-style scanner bucket `Cup and Handle Pattern in Force`.
- The bullish trigger is a weekly breakout above `1027.22`.
- A simple measured target after confirmation is `1231.42`.
- The setup weakens if price loses the handle low near `899.0`.
- Visible inside the one-year chart: yes.

## Caveats

- cup has a declining left side and rising right side
- handle remains in upper half of the cup
- cup is shorter than TradingView's 20-bar auto-pattern minimum
- right rim is below the left rim, so this is an in-progress/looser read
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
| 1 | 75.04 | Cup and Handle Pattern in Force | 2026-01-12 -> 2026-03-09 -> 2026-04-20; handle low 2026-05-04 | 1027.22 |
| 2 | 74.18 | Cup and Handle Pattern in Force | 2026-02-09 -> 2026-03-09 -> 2026-04-20; handle low 2026-05-04 | 1027.22 |
| 3 | 66.95 | Cup and Handle Pattern in Force | 2025-12-08 -> 2026-03-09 -> 2026-04-20; handle low 2026-05-04 | 1027.22 |
| 4 | 56.6 | Cup and Handle Pattern in Force | 2025-09-22 -> 2025-11-17 -> 2026-04-20; handle low 2026-05-04 | 1027.22 |
