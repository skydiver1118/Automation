# Stock Project V2.0 — one-time automation setup

The repository code now supports all recurring functions requested: actual NYSE trading-date gating, score/history persistence, a dashboard with per-stock detail pages, GitHub Pages publishing, and email delivery.

## 1. Email secret

The workflow sends the results link to `1118xmb@gmail.com` through Gmail SMTP.

In GitHub open:

`Automation` → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Create these two secrets:

- `STOCK_EMAIL_USERNAME` — the Gmail account that will send the message (it can be `1118xmb@gmail.com`).
- `STOCK_EMAIL_APP_PASSWORD` — a Google **App Password**, not the normal Gmail password. The Google account must have 2-Step Verification enabled before an App Password can be generated.

Do not commit the App Password to the repository.

## 2. Dashboard web link / GitHub Pages

The workflow publishes `stock-project-v2/dashboard/` to the `gh-pages` branch after a valid trading-session refresh.

After the workflow has created the `gh-pages` branch, open:

`Automation` → **Settings** → **Pages**

Set the publishing source to **Deploy from a branch**, select `gh-pages`, and select `/ (root)`.

The intended dashboard URL is:

`https://skydiver1118.github.io/Automation/`

The email also contains a GitHub fallback link to the committed dashboard files.

Because `Automation` is a private repository, GitHub Pages availability depends on the GitHub account/plan. If Pages cannot be enabled for the private repository, use a public site repository for the dashboard while keeping the engine/data private.

## 3. Trading-date logic

The cron trigger runs only on weekdays to reduce unnecessary Actions usage, but weekday is **not** considered sufficient. Before doing any market work, the workflow queries the NYSE exchange calendar with `pandas_market_calendars`.

This correctly skips exchange holidays and records the scheduled NYSE close time, including early-close sessions. `run_v2.py` then performs a second guard: it refuses to persist a result until the market-data feed contains the completed session for that actual trading date.

Thus a score update requires both:

1. the date is an actual NYSE session, and
2. completed benchmark/session data for that date is available.

## 4. Dashboard

`dashboard.py` creates:

- `dashboard/index.html` — main dashboard
- `dashboard/stocks/NVDA.html`
- `dashboard/stocks/MU.html`
- `dashboard/stocks/SPCX.html`
- `dashboard/stocks/LITE.html`
- `dashboard/stocks/META.html`
- `dashboard/stocks/NBIS.html`
- `dashboard/stocks/MRVL.html`
- `dashboard/stocks/RKLB.html`
- `dashboard/stocks/AXTI.html`
- `dashboard/stocks/APLD.html`
- `dashboard/stocks/IREN.html`

The main page includes the current ranking, Long-Term / Short-Term / Buy-Now scores, valuation/quality/growth/technical factors, market cap, RSI, and an interactive score-history chart at the top. The chart lets the viewer switch between Buy-Now, Long-Term, and Short-Term histories.

Each ticker links to its own detail page containing score history, factor-score bars, relative strength, RSI/MACD/ADX, 20/50/200DMA distances, growth/revisions, valuation multiples, FCF metrics, margins, and ROIC proxy.

## 5. Historical series

Every completed trading session is retained as:

`stock-project-v2/history/YYYY-MM-DD.csv`

Dashboard charts are rebuilt from the complete history directory. This means score movement is preserved indefinitely and the line graph grows automatically after each valid trading day.

## 6. Schedule

Current scheduled run: Monday–Friday at `23:15 UTC`, followed by NYSE-calendar and completed-data checks. No score, dashboard email, or dated history record is generated for non-trading dates.
