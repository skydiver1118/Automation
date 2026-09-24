# Multi Bagger Methodology v2.2 — 5x Feasibility Shadow Layer

## Status
**Shadow / validation mode.** Approved for research and dashboard comparison, but it MUST NOT replace production v2.1 ranking until the historical calibration gate below is satisfied. v2.1 remains reproducible and unchanged.

## Why v2.2 exists
The v2.1 specification describes its 15% valuation factor as "valuation/starting market cap", but the frozen production calculator actually uses only EV / forward gross profit and FCF yield. It contains no explicit starting-market-cap or required-5x-value calculation.

That omission can rank an excellent mega-cap business as the best "Multi Bagger" candidate even when a fivefold outcome requires several trillion dollars of additional equity value. v2.2 separates business quality from return feasibility rather than applying an arbitrary large-cap exclusion.

## Outputs
1. **MB Quality Score (0–100)** — existing frozen v2.1 eight-factor score; never rewritten.
2. **5x Feasibility Score (0–100)** — new shadow score.
3. **5x Required Market Cap** = current market cap × 5.
4. **Supportable 5Y Market Cap** — scenario output, not a price target.
5. **Supportable 5Y Multiple** = supportable 5Y market cap / current market cap.
6. **Feasibility gap** = supportable 5Y multiple / 5.
7. **Final Multi-Bagger Score** — withheld until calibration. Do not manufacture a probability or production rank from the shadow layer.

## Five-year operating scenario
For an operating company with positive or plausibly positive normalized earnings:
- Revenue_5 = Revenue_TTM × (1 + normalized_revenue_CAGR)^5
- Earnings_5 = Revenue_5 × normalized_net_margin
- EquityValue_5 = Earnings_5 × terminal_PE
- Supportable5xMultiple = EquityValue_5 / CurrentMarketCap

Where sector economics make earnings inappropriate, use a separately documented EV-based model and bridge net debt/economic claims explicitly.

### Scenario discipline
Use three scenarios and record every assumption:
- Bear: conservative normalized growth, margins and terminal multiple.
- Base: evidence-supported normalized economics, explicitly lower than transient peak conditions when cyclicality is material.
- Bull: plausible upside, not an unconstrained continuation of the latest growth rate.

Distinguish reported/consensus inputs from analyst assumptions.

## Shadow feasibility score
Until empirically calibrated, use a transparent monotonic mapping of the **base supportable 5Y multiple** only for diagnostic comparison:

| Supportable 5Y multiple | Shadow feasibility score |
| ---: | ---: |
| <=1.0x | 0 |
| 1.5x | 15 |
| 2.0x | 30 |
| 3.0x | 50 |
| 4.0x | 70 |
| 5.0x | 85 |
| >=7.0x | 100 |

Interpolate linearly. This is **uncalibrated**, is not P(5x), and cannot promote/demote membership by itself.

## Starting-size diagnostics
Always display current market cap, required 5x market cap, incremental equity value required, current revenue, normalized 5Y revenue, normalized margin, and terminal multiple assumptions.

Market cap is an economic hurdle, not a hard penalty. A $1T company can score well only if supportable five-year economics plausibly bridge to the required value.

## Dilution and capital intensity
Fivefold feasibility is measured per current share/equity claim, not enterprise growth. Material expected dilution must reduce supportable per-share value. Where future financing needs are substantial, include a dilution/capital-claims adjustment or retain Research Hold.

## Historical calibration gate
Before v2.2 can become production:
1. Assemble a point-in-time, survivorship-bias-safe U.S. equity sample with market cap, shares, fundamentals, and delisting-adjusted total returns.
2. Use only information available at each formation date.
3. Define outcome as forward 5-year total return >=5x, with secondary 3x and catastrophic-loss outcomes.
4. Split chronologically into development and untouched out-of-sample periods.
5. Compare v2.1 vs candidate v2.2 on precision/recall, top-decile 5x hit rate, median/mean forward return, mega-cap false positives, permanent-loss incidence, and calibration by starting-market-cap bucket.
6. Test sensitivity to feasibility anchors, scenario assumptions and sector model.
7. Adopt only if v2.2 improves 5x identification out of sample without unacceptable deterioration in coverage or false negatives.

Current repository data do not satisfy this calibration gate. Do not call a same-universe or current-winner retrospective a valid historical backtest.

## Migration rule
Production v2.1 files and scores are immutable historical evidence. v2.2 must use a new methodology identifier and new output fields. Never silently rewrite v2.1 scores.

Approved: 2026-09-24, prompted by the MU starting-market-cap contradiction.
