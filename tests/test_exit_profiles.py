from __future__ import annotations

import pandas as pd
import pytest

from src.strategy_lab.exit_profiles import (
    calculate_atr,
    render_profiles_markdown,
    simulate_long_exit,
    top_loss_taking_profiles,
    top_profit_taking_profiles,
)


def test_profile_catalog_has_top_three_profit_and_loss_profiles() -> None:
    profit_profiles = top_profit_taking_profiles()
    loss_profiles = top_loss_taking_profiles()

    assert [profile.rank for profile in profit_profiles] == [1, 2, 3]
    assert [profile.rank for profile in loss_profiles] == [1, 2, 3]
    assert profit_profiles[0].key == "risk_first_trend_runner"
    assert loss_profiles[0].key == "one_r_invalidation"


def test_atr_uses_gap_aware_true_range() -> None:
    dates = pd.date_range("2026-01-01", periods=3, freq="D")
    ohlc = pd.DataFrame(
        {
            "High": [11.0, 15.0, 14.0],
            "Low": [9.0, 13.0, 12.0],
            "Close": [10.0, 14.0, 13.0],
        },
        index=dates,
    )

    atr = calculate_atr(ohlc, period=2)

    assert atr.iloc[0] == 2.0
    assert atr.iloc[1] == 3.5
    assert atr.iloc[2] == 3.5


def test_simulate_long_exit_scales_out_and_raises_stop() -> None:
    dates = pd.date_range("2026-01-01", periods=5, freq="D")
    ohlc = pd.DataFrame(
        {
            "High": [101.0, 111.0, 121.0, 125.0, 126.0],
            "Low": [99.0, 108.0, 118.0, 119.0, 117.0],
            "Close": [100.0, 110.0, 120.0, 123.0, 118.0],
        },
        index=dates,
    )

    result = simulate_long_exit(ohlc, entry_price=100.0, initial_stop=90.0)

    assert [(event.action, round(event.fraction, 4), event.reason) for event in result.events[:2]] == [
        ("scale_out", 0.3333, "recover risk"),
        ("scale_out", 0.3333, "lock profit"),
    ]
    assert result.remaining_fraction == pytest.approx(1 / 3)
    assert result.active_stop >= 110.0


def test_simulate_long_exit_supports_time_failure_exit() -> None:
    dates = pd.date_range("2026-01-01", periods=4, freq="D")
    ohlc = pd.DataFrame(
        {
            "High": [101.0, 102.0, 103.0, 104.0],
            "Low": [99.0, 99.0, 99.0, 99.0],
            "Close": [100.0, 101.0, 102.0, 103.0],
        },
        index=dates,
    )

    result = simulate_long_exit(ohlc, entry_price=100.0, initial_stop=90.0, max_bars_without_half_r=3)

    assert result.events[-1].action == "time_exit"
    assert result.events[-1].fraction == 1.0
    assert result.remaining_fraction == 0.0


def test_render_profiles_markdown_includes_profile_names() -> None:
    markdown = render_profiles_markdown()

    assert "Risk-First Trend Runner" in markdown
    assert "One-R Invalidation Stop" in markdown
