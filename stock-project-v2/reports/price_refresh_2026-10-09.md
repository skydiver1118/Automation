# October 9 price-refresh investigation and bounded mitigation

This change mitigates repeat failures and protects publication. It does **not** establish a permanently available replacement for Yahoo's missing daily bars.

## Reproduced mechanism

[Run 37865192683](https://github.com/skydiver1118/Automation/actions/runs/37865192683) rejected all 25 configured securities and SMH/QQQ for October 8. The latest daily rows contained volume, but adjusted OHLC was nonfinite. Prior failures include [37711438296](https://github.com/skydiver1118/Automation/actions/runs/37711438296) and [37554235245](https://github.com/skydiver1118/Automation/actions/runs/37554235245).

Fresh direct Yahoo chart responses for NVDA, SMH, and SPCX contained null Close and Adj Close before yfinance parsing. OHLC normalization and adjustment did not introduce the missing close. Both query1 and query2 reproduced it. Five-day, one-month, two-year, five-year and explicit date windows also reproduced it; no-cache requests returned responses with Age 0-2 seconds and the same nulls. Public Yahoo historical tables stopped at October 7. The public CSV endpoint returned HTTP 401; no authentication or credential changes were attempted.

The captured production tails for **all 27 series** are replayed in tests. A separate raw Yahoo fixture reproduces null Close/Adj Close turning all adjusted OHLC into NaN. The full-universe test proves ranking is never called and saved files are unchanged when these responses recur. No intraday or repair-mode request is enabled.

## Why repair=True is excluded

The documented yfinance repair mode reconstructs missing daily data using finer intervals. In the live experiment it produced NVDA 230.7446, SMH 606.68 and SPCX 164.35. These differ from independently observed regular-session closes (230.48, 607.27 and 160.57 respectively). The first two also disagree with Yahoo chart metadata. Finite output alone is not sufficient evidence of the intended regular-session close.

[The yfinance documentation](https://ranaroussi.github.io/yfinance/advanced/price_repair.html) explicitly warns reconstructed prices can differ from subsequently corrected Yahoo daily data. Repair mode is not used by this patch. Quote metadata contains a regular-market price/time, but does not establish a complete dividend/capital-gain-adjusted daily series; it is not substituted for Adj Close. Independent Stock Analysis samples supplied during the investigation are diagnostic only: permitted automated access, precision and adjustment semantics have not been established. No cross-provider rows are spliced into Yahoo history.

## Candidate behavior

- Scheduled runs use the existing latest-completed-session and same-method/universe reuse mechanism. Reuse additionally requires a price column with finite positive values.
- A current score CSV alone does not suppress downstream rebuilding: a new read-only validator also checks the dashboard CSV, investment JSON, entry analysis and canonical layer for exact universe, matching session, matching prices/scores, and current support/entry series.
- When the complete current snapshot is reusable, scheduled runs skip network-dependent recomputation and dashboard rebuilding. They still validate and may republish the saved assets, allowing recovery from an earlier deployment failure.
- Before any publication, the same validator rejects incomplete or mixed-session artifacts. Data retrieval failure still fails the job before publication.
- One bounded catch-up is added at 02:30 UTC Tuesday-Saturday (21:30/22:30 New York on the preceding trading day). It targets the latest completed NYSE session even if GitHub queues it past local midnight. It is an additional opportunity for finalized daily data, not a guarantee of Yahoo availability. There is no indefinite retry loop.
- Push-triggered production publication is restricted to main so a review branch cannot deploy to the shared gh-pages branch.

Scoring functions, configured universe, adjusted-price requests, corporate-action handling, freshness rules, credentials and broker/scanner systems are unchanged. Scoring fingerprint remains `2b1cdf0a1d18475acdb6`.

## Verification and rollout boundary

Offline tests cover invalid cached prices, the actual scheduled invocation, all 27 captured failures, stale support data, inconsistent dashboard prices, and read-only validation. The workflow is checked with actionlint and a scenario check for fresh/reused sessions and a catch-up delayed into Saturday. The existing October 6 complete snapshot passes the new artifact validator.

The isolated live full refresh attempted during this investigation failed closed on the unavailable October 8 daily closes. The previous CSV, JSON and history hashes remained unchanged. Therefore a successful fresh current-session end-to-end run remains blocked by upstream data, and this must not be presented as a permanent price-feed fix.

The candidate is for draft review. Do not merge or dispatch a production run without the coordinating task's explicit go-ahead. Proposed next production action, after review: merge this exact tested branch into main and allow the automatic push workflow to perform one guarded refresh; do not additionally dispatch a duplicate run. If fresh daily data is still unavailable, retain the prior publication and report the failure. A new data provider or reconstructed-price policy requires separate validation and approval.
