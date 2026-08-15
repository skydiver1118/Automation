# Stock Technical Analysis Framework

This framework classifies a stock as Bullish, Neutral, or Bearish, then proposes buy-entry zones only when the setup has enough trend, momentum, volume, and risk confirmation. It is technical strategy research, not investment advice.

## Source Research

The source weighting is intentionally uneven:

| Source type | Role in the framework | Links |
| --- | --- | --- |
| GitHub/open-source TA libraries | Define a standard, reproducible indicator set rather than inventing custom formulas. | [bukosabino/ta](https://github.com/bukosabino/ta), [TA-Lib](https://ta-lib.org/index.html) |
| Reddit practitioner discussion | Treat support/resistance, position sizing, and historical validation as required parts of the workflow, not afterthoughts. | [r/technicalanalysis guide](https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/) |
| X/Twitter public examples | Use only as sentiment/workflow sampling. Public X text is limited without login, so it is not treated as authoritative evidence. | [X/Grok-indexed TA example](https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj), [X search path](https://x.com/search?q=%22RSI%22%20%22MACD%22%20%22moving%20averages%22%20%22technical%20analysis%22&src=typed_query&f=live) |
| Canonical book reference | Anchor the classic TA categories: trend, volume, moving averages, oscillators, money management, and tactics. | [John J. Murphy, Technical Analysis of the Financial Markets](https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/) |

## Data Policy

- Fetch at least 2 years of daily OHLCV data so SMA200 and long context are valid.
- Plot only the latest 3 calendar months of daily data, matching the requested graph window.
- Use adjusted daily OHLCV from yfinance for split/dividend-adjusted continuity.
- Reject analysis if there are fewer than 30 fully indicator-ready rows.

## Indicator Stack

| Category | Indicators | Purpose |
| --- | --- | --- |
| Trend | SMA20, SMA50, SMA200, EMA8, EMA21 | Identify direction, dynamic support, and trend repair/failure. |
| Momentum | RSI14, MACD 12/26/9, 20-day ROC | Confirm whether price movement has follow-through. |
| Volatility | Bollinger Bands 20/2, ATR14 | Avoid overextended buys and size stops realistically. |
| Directional strength | ADX14, +DI, -DI | Separate weak rebounds from directional trends. |
| Volume | Volume20, OBV, up-volume/down-volume ratio | Confirm breakouts and accumulation/distribution. |
| Levels | Pivot highs/lows, 20-day high, 63-day high/low | Build practical support, resistance, and entry zones. |

## Bullish Classification

The framework uses a 100-point score plus hard gates.

| Bucket | Max points | Main checks |
| --- | ---: | --- |
| Trend | 40 | Close above SMA20/50/200, SMA20>SMA50, SMA50>SMA200, rising SMA50. |
| Momentum | 25 | RSI constructive, MACD above signal, MACD histogram improving, positive 20-day ROC. |
| Confirmation | 15 | Above-average volume, OBV above its average, up-volume greater than down-volume. |
| Risk/context | 20 | ADX/+DI confirmation, not dangerously extended, manageable ATR, close near 63-day high. |

Labels:

- Bullish: score >= 70, close above SMA50, and MACD above signal.
- Neutral: score is mixed, or score is high but a hard gate is missing.
- Bearish: score < 45, or close is below SMA50 while MACD is below signal.

The hard gates are deliberate. A chart can have a high score from trend history but still be Neutral if current momentum has rolled over.

## Buy Entry Rules

The framework never treats a bullish label as an immediate market buy. It creates conditional entry zones:

| Entry type | When to use | Buy trigger | Stop logic |
| --- | --- | --- | --- |
| Pullback entry | Bullish or neutral-bullish chart pulling into EMA21/SMA20/support. | Price holds the zone and closes back above the prior day's high or EMA8. | Below nearest support/SMA50 minus 1 ATR. |
| Breakout entry | Price is pressing resistance or a 20/63-day high. | Daily close above resistance with volume above Volume20 and positive MACD histogram. | Below breakout support or roughly 2 ATR below close. |
| Reclaim entry | Bearish or damaged chart that is repairing. | Daily close back above SMA20/SMA50 with MACD above signal. | Below the reclaim level minus 1.5 ATR. |

Every entry plan must show:

- Entry zone, not a single price.
- Trigger condition.
- Stop level.
- Target 1 near 2R or next resistance.
- Target 2 near 3R or higher resistance.
- Invalidation rule.

## Output Artifacts

The implemented script is:

```powershell
python scripts\stock_technical_framework.py --ticker NVDA --out-dir reports\technical_framework --chart-months 3
```

Outputs:

- Three-month daily chart with Close, EMA8, EMA21, SMA50, SMA200, Bollinger Bands, volume, RSI, MACD, support/resistance, and entry zones.
- Markdown sample report with decision, score breakdown, support/resistance, and entry plans.

## Operational Notes

- Treat Reddit and X as qualitative signal sources only. They can reveal popular heuristics and sentiment, but they do not validate an entry.
- Validate setups historically before using real capital. At minimum, log each signal, entry, stop, target, and 10/20/40-day outcome.
- Avoid buys directly into earnings or major binary events unless that event risk is intentionally part of the plan.
- Cap per-trade risk before share sizing. A common practitioner rule is 1%-2% of account equity per trade, adjusted for the user's actual risk tolerance.
