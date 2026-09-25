# Multi-Bagger v2.2 Free-Data Calibration Plan

## Objective
Calibrate the 5x-feasibility layer using only free/public resources while preserving point-in-time discipline and exposing unavoidable coverage gaps.

## Source stack

### 1. SEC EDGAR — authoritative fundamentals
Use:
- Financial Statement Data Sets (quarterly ZIPs, 2009-present)
- Submissions API / submissions bulk ZIP
- Companyfacts API for spot reconciliation

Why:
- as-filed values;
- filing dates are explicit;
- no API key;
- suitable for point-in-time financial reconstruction.

Limitations:
- no clean historical security-master with permanent ticker mapping;
- non-XBRL/foreign/older filings have uneven coverage;
- normalization across custom tags still requires reconciliation.

### 2. Stooq — free long-run U.S. price history
Use the U.S. daily bulk archive when accessible.

Why:
- broad U.S. history;
- long daily history;
- free public download for personal research.

Limitations:
- not a CRSP-quality delisting-return source;
- corporate-action/terminal-value treatment for acquired/delisted names must be checked;
- automated bulk access may be rate/CAPTCHA constrained.

### 3. Alpha Vantage listing-status endpoint — optional free enhancement
A free API key can provide active/delisted symbol lists as-of historical dates from 2010. This is useful for survivorship diagnostics but is not required for the SEC fundamentals pipeline.

### 4. SimFin free tier — optional cross-check
Use only for spot-checking reconstructed SEC metrics or survivorship diagnostics. The free tier's limited historical depth is not sufficient for the main 5-year calibration.

## Free-data study design

### Formation dates
Annual June 30 snapshots, 2010-2021.

### Point-in-time rule
A filing is usable only when filed <= formation_date. No later restatement can replace the historical value unless the original filing is retained as a separate observation.

### Minimum factors
- market cap
- revenue TTM
- revenue growth
- operating margin
- FCF / cash-flow proxy
- cash
- debt
- shares outstanding / dilution
- valuation proxy
- sector/SIC

### Outcomes
Primary: 5-year total price multiple where price/corporate-action history is reliable.
Secondary: 3-year multiple; catastrophic-loss / terminal-security flags.

### Coverage flags
Every row must carry:
- ticker_cik_match_confidence
- price_history_complete
- terminal_value_verified
- corporate_action_verified
- fundamentals_point_in_time
- outcome_usable

Rows failing outcome verification are excluded from calibrated hit-rate denominators, never treated as zero-return failures.

## Historical starting-size buckets
- < $500M
- $500M-$1B
- $1B-$5B
- $5B-$20B
- $20B-$50B
- $50B-$100B
- $100B-$250B
- $250B-$500B
- $500B-$1T
- > $1T

## Validation outputs
For every bucket and model decile:
- N
- 3x hit rate
- 5x hit rate
- median 5Y multiple
- mean 5Y multiple
- catastrophic-loss rate
- excluded/unverifiable rate

Compare:
1. v2.1 Quality only
2. Quality + raw size penalty
3. Quality + v2.2 supportable-value feasibility

## Production gate
The free-data study may promote v2.2 to production only if point-in-time rules pass, outcome verification coverage is high enough to avoid material selection bias, v2.2 improves untouched out-of-sample 5x identification, and results are not driven only by excluding unverifiable delistings.

If these conditions fail, v2.2 remains shadow and the dashboard must state that a CRSP/Compustat-grade validation is still required.
