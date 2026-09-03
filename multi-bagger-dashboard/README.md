# Multi Bagger Top-20 Dashboard

This is a standalone dashboard for the Multi Bagger six-pass research archive.

## Published dashboard

- Multi Bagger: `https://skydiver1118.github.io/Automation/multi-bagger/`
- Stock Project V2 remains separate: `https://skydiver1118.github.io/Automation/stock-project-v2/`

## Source boundaries

- Dashboard source: `multi-bagger-dashboard/index.html`
- Canonical data: `stock-project-v2/data/multi_bagger/`
- Dated reports: `stock-project-v2/reports/multi_bagger/`
- Publisher: `.github/workflows/multi-bagger-dashboard.yml`

The Multi Bagger publisher writes only the `multi-bagger/` directory on the `gh-pages` branch. The Stock Project V2 publisher writes `stock-project-v2/`. Both preserve sibling directories.

## Price column

- `build_price_snapshot.py` retrieves the regular-session close for the dashboard snapshot's `market_session_date`.
- Published price data is stored separately at `multi-bagger/data/prices/latest.json`.
- Price data does not come from, modify, or merge with the Stock Project V2 dashboard.

## Run timestamp

- The Snapshot card displays the research run date, hour, and minute from `recorded_at`.
- The timestamp is formatted in `America/New_York` and includes the active Eastern time-zone abbreviation.
- The market-session date remains separately labeled beside the run timestamp.
