from src.strategy_lab.owned_stocks_sma50_alert import SmaStatus, build_email, load_symbols


def test_load_symbols_normalizes_and_deduplicates() -> None:
    assert load_symbols({"symbols": [" qqq ", "SOXL", "qqq"]}) == ["QQQ", "SOXL"]


def test_build_email_marks_added_blue_and_removed_red_strike() -> None:
    statuses = [
        SmaStatus(symbol="QQQ", price=90.0, sma50=100.0, below_sma50=True, bar_date="2026-05-26"),
        SmaStatus(symbol="SOXL", price=50.0, sma50=40.0, below_sma50=False, bar_date="2026-05-26"),
    ]

    plain, html = build_email(statuses, previous_below={"SOXL"})

    assert "New below SMA50: QQQ" in plain
    assert "Removed from below SMA50: SOXL" in plain
    assert "color:#1d4ed8" in html
    assert "QQQ" in html
    assert "color:#b91c1c" in html
    assert "text-decoration:line-through" in html
    assert "SOXL" in html
