# Stock Project V2.0

Repeatable ranking engine for the 11-stock AI / semiconductor / infrastructure universe.

## Core universe

NVDA, MU, SPCX, LITE, META, NBIS, MRVL, RKLB, AXTI, APLD, IREN

ORCL is excluded.

## Headline scores

Each trading-date refresh produces:

- **Long-Term Score (0–100):** 5–10 year risk-adjusted compounding potential.
- **Short-Term Score (0–100):** approximately 1–3 month momentum / technical attractiveness.
- **Buy-Now Score (0–100):** current capital-allocation attractiveness.

## V2 factor set

### Long-Term
- Forward revenue growth
- Forward EPS growth
- 30/60/90-day revenue and EPS revisions
- ROIC
- FCF margin / FCF yield
- Gross and operating margins
- Balance-sheet quality and dilution
- Forward P/E
- EV/Sales
- EV/EBITDA when meaningful
- Growth-adjusted valuation
- Secular / competitive durability

### Short-Term
- 1M / 3M / 6M / 12M relative strength vs SMH and QQQ
- RSI
- MACD
- ADX
- Distance from 20DMA / 50DMA / 200DMA
- Volume / breakout confirmation
- Near-term estimate revisions

## Relative-strength formula

RS_h = 0.67 × (Stock Return_h − SMH Return_h) + 0.33 × (Stock Return_h − QQQ Return_h)

Horizon weights: 1M 15%, 3M 30%, 6M 30%, 12M 25%.

## Buy-Now formula

BuyNow = 55% × LongTerm + 30% × ShortTerm + 15% × Entry/Valuation

## Data-quality rules

- Use point-in-time data where possible.
- Do not backfill future analyst estimates into past dates.
- Missing history (for example a recently listed stock) remains NA and its factor weight is neutralized / redistributed; do not invent data.
- Winsorize extreme factor values before cross-sectional standardization.
- Record source timestamps and the market close used for each refresh.
- Only generate a dated ranking for an actual U.S. trading day.

## Refresh cadence

Refresh after each U.S. trading session. Store the current ranking in `latest_scores.csv` and, when the automation writes historical outputs, preserve a dated snapshot under `history/`.
