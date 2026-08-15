from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

import pandas as pd


ProfileCategory = Literal["profit", "loss"]


@dataclass(frozen=True)
class ScaleOutRule:
    """Reduce position size after a trade reaches a profit multiple."""

    trigger_r: float
    fraction: float
    stop_r: float | None = None
    label: str = ""


@dataclass(frozen=True)
class TrailingRule:
    method: Literal["chandelier", "ema", "structure"]
    atr_period: int | None = None
    atr_multiple: float | None = None
    ema_period: int | None = None
    swing_lookback: int | None = None
    activation_r: float = 0.0


@dataclass(frozen=True)
class ExitProfile:
    rank: int
    category: ProfileCategory
    key: str
    name: str
    objective: str
    rules: tuple[str, ...]
    best_for: str
    avoid_when: str
    scale_outs: tuple[ScaleOutRule, ...] = ()
    trailing_rule: TrailingRule | None = None


@dataclass(frozen=True)
class ExitEvent:
    date: pd.Timestamp
    action: Literal["scale_out", "stop_exit", "time_exit"]
    fraction: float
    price: float
    r_multiple: float
    reason: str


@dataclass(frozen=True)
class ExitSimulation:
    events: tuple[ExitEvent, ...]
    remaining_fraction: float
    active_stop: float


def top_profit_taking_profiles() -> tuple[ExitProfile, ...]:
    return (
        ExitProfile(
            rank=1,
            category="profit",
            key="risk_first_trend_runner",
            name="Risk-First Trend Runner",
            objective="Recover open risk quickly, then let the largest trend leg pay.",
            rules=(
                "At +1R, sell one third and raise the stop to breakeven.",
                "At +2R, sell one third and raise the stop to +1R.",
                "Hold the final third while price respects EMA20 or a 3 ATR Chandelier stop.",
                "Exit the runner only after trend structure breaks, not because price feels high.",
            ),
            best_for="Momentum breakouts, SOXL/TQQQ-style trend bursts, and strategies where a few large wins drive expectancy.",
            avoid_when="Mean-reversion systems with short holding periods and no trend persistence.",
            scale_outs=(
                ScaleOutRule(trigger_r=1.0, fraction=1 / 3, stop_r=0.0, label="recover risk"),
                ScaleOutRule(trigger_r=2.0, fraction=1 / 3, stop_r=1.0, label="lock profit"),
            ),
            trailing_rule=TrailingRule(method="chandelier", atr_period=22, atr_multiple=3.0, activation_r=2.0),
        ),
        ExitProfile(
            rank=2,
            category="profit",
            key="volatility_ladder",
            name="Volatility Ladder",
            objective="Take earlier profits during volatility expansion while preserving a runner.",
            rules=(
                "At +1.5R, sell 25% and move the stop to breakeven.",
                "At +3R, sell 25% and trail the rest by the highest close minus 2.5 ATR.",
                "Widen to 3 ATR when ATR is rising faster than price, so a strong but noisy trend can breathe.",
                "Never lower the trailing stop after it has ratcheted upward.",
            ),
            best_for="Leveraged ETFs, high-beta stocks, crypto, and names whose normal pullbacks are too large for fixed stops.",
            avoid_when="Low-volatility scalps where ATR estimates are unstable or too small.",
            scale_outs=(
                ScaleOutRule(trigger_r=1.5, fraction=0.25, stop_r=0.0, label="first volatility pay"),
                ScaleOutRule(trigger_r=3.0, fraction=0.25, stop_r=1.5, label="second volatility pay"),
            ),
            trailing_rule=TrailingRule(method="chandelier", atr_period=14, atr_multiple=2.5, activation_r=1.5),
        ),
        ExitProfile(
            rank=3,
            category="profit",
            key="structure_ladder",
            name="Structure Ladder",
            objective="Use market structure, not a fixed target, to decide whether profit remains worth holding.",
            rules=(
                "At the first major resistance or +2R, sell 30%.",
                "After each higher low, trail the stop under that swing with at least a 1 ATR floor.",
                "Keep the runner while higher highs and higher lows continue.",
                "Exit the runner on failed breakout, lower high, and close below EMA20.",
            ),
            best_for="Swing trades with clean support/resistance levels and visible stair-step trends.",
            avoid_when="Choppy instruments that make many false swing highs and lows.",
            scale_outs=(ScaleOutRule(trigger_r=2.0, fraction=0.30, stop_r=0.5, label="structure pay"),),
            trailing_rule=TrailingRule(method="structure", swing_lookback=5, activation_r=2.0),
        ),
    )


def top_loss_taking_profiles() -> tuple[ExitProfile, ...]:
    return (
        ExitProfile(
            rank=1,
            category="loss",
            key="one_r_invalidation",
            name="One-R Invalidation Stop",
            objective="Make the maximum normal loss known before entry.",
            rules=(
                "Set the initial stop where the trade idea is wrong, not where the pain feels tolerable.",
                "Use position size so the stop equals the chosen account risk, commonly 0.25% to 1%.",
                "Use at least a 1 ATR floor so normal noise does not trigger the stop.",
                "Exit fully if the stop is touched or breached at the close-based execution point.",
            ),
            best_for="All systematic strategies as the first line of defense.",
            avoid_when="The invalidation level is so far away that position size becomes impractically small.",
        ),
        ExitProfile(
            rank=2,
            category="loss",
            key="trend_structure_break",
            name="Trend Structure Break",
            objective="Leave when the trend thesis has stopped working, even if the 1R stop has not been hit.",
            rules=(
                "Exit or cut exposure when price closes below EMA20 after a failed reclaim.",
                "Confirm with lower high/lower low behavior, RSI below 50, or expanding down-volume.",
                "For leveraged ETFs, treat a broad-market trend break as a portfolio-level exit.",
                "Re-entry requires a fresh trend signal, not an immediate revenge buy.",
            ),
            best_for="Trend-following and momentum rotation systems.",
            avoid_when="Mean-reversion entries that intentionally buy below moving averages.",
            trailing_rule=TrailingRule(method="ema", ema_period=20, activation_r=0.0),
        ),
        ExitProfile(
            rank=3,
            category="loss",
            key="time_and_volatility_failure",
            name="Time And Volatility Failure",
            objective="Remove capital from trades that fail to confirm soon enough.",
            rules=(
                "If the trade cannot reach +0.5R within the planned confirmation window, exit or halve it.",
                "If ATR expands against the position while price makes no progress, reduce risk.",
                "If the position gaps through the initial stop, exit at the first executable price and log slippage.",
                "Use this as a secondary filter, never as permission to ignore the initial stop.",
            ),
            best_for="Breakouts, opening-range trades, and fast momentum systems.",
            avoid_when="Slow monthly rotation systems where the edge intentionally develops over many weeks.",
        ),
    )


def all_exit_profiles() -> tuple[ExitProfile, ...]:
    return top_profit_taking_profiles() + top_loss_taking_profiles()


def calculate_atr(ohlc: pd.DataFrame, period: int = 14) -> pd.Series:
    high = ohlc["High"].astype(float)
    low = ohlc["Low"].astype(float)
    close = ohlc["Close"].astype(float)
    prior_close = close.shift(1)
    true_range = pd.concat(
        [
            high - low,
            (high - prior_close).abs(),
            (low - prior_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return true_range.rolling(period, min_periods=1).mean()


def simulate_long_exit(
    ohlc: pd.DataFrame,
    entry_price: float,
    initial_stop: float,
    profit_profile: ExitProfile | str = "risk_first_trend_runner",
    *,
    max_bars_without_half_r: int | None = None,
) -> ExitSimulation:
    """Simulate long-side scale-outs and trailing stops for one open position.

    The simulation is deliberately conservative and end-of-day oriented: scale-outs
    trigger from closes, while stop exits trigger from lows at the active stop.
    """

    if entry_price <= initial_stop:
        raise ValueError("entry_price must be greater than initial_stop for a long trade")
    if ohlc.empty:
        raise ValueError("ohlc must contain at least one row")

    profile = _resolve_profit_profile(profit_profile)
    risk = entry_price - initial_stop
    active_stop = float(initial_stop)
    remaining = 1.0
    events: list[ExitEvent] = []
    triggered: set[float] = set()
    highest_close = float(entry_price)
    atr = calculate_atr(ohlc, profile.trailing_rule.atr_period if profile.trailing_rule and profile.trailing_rule.atr_period else 14)

    for bar_number, (date, row) in enumerate(ohlc.iterrows(), start=1):
        close = float(row["Close"])
        low = float(row["Low"])
        highest_close = max(highest_close, close)

        if low <= active_stop and remaining > 0:
            events.append(
                ExitEvent(
                    date=pd.Timestamp(date),
                    action="stop_exit",
                    fraction=remaining,
                    price=active_stop,
                    r_multiple=(active_stop - entry_price) / risk,
                    reason="active stop breached",
                )
            )
            remaining = 0.0
            break

        current_r = (close - entry_price) / risk
        if max_bars_without_half_r is not None and bar_number >= max_bars_without_half_r and current_r < 0.5 and remaining > 0:
            events.append(
                ExitEvent(
                    date=pd.Timestamp(date),
                    action="time_exit",
                    fraction=remaining,
                    price=close,
                    r_multiple=current_r,
                    reason="failed to reach +0.5R inside confirmation window",
                )
            )
            remaining = 0.0
            break

        for rule in profile.scale_outs:
            if rule.trigger_r in triggered or current_r < rule.trigger_r or remaining <= 0:
                continue
            fraction = min(rule.fraction, remaining)
            remaining = max(0.0, remaining - fraction)
            triggered.add(rule.trigger_r)
            events.append(
                ExitEvent(
                    date=pd.Timestamp(date),
                    action="scale_out",
                    fraction=fraction,
                    price=close,
                    r_multiple=current_r,
                    reason=rule.label or f"reached +{rule.trigger_r:g}R",
                )
            )
            if rule.stop_r is not None:
                active_stop = max(active_stop, entry_price + rule.stop_r * risk)

        active_stop = max(
            active_stop,
            _trailing_stop(
                profile.trailing_rule,
                ohlc.loc[:date],
                highest_close,
                float(atr.loc[date]),
                entry_price,
                risk,
            ),
        )

    return ExitSimulation(events=tuple(events), remaining_fraction=remaining, active_stop=active_stop)


def render_profiles_markdown(profiles: Iterable[ExitProfile] | None = None) -> str:
    selected = tuple(profiles) if profiles is not None else all_exit_profiles()
    lines = [
        "# Profit Taking And Loss Taking Exit Profiles",
        "",
        "Built from the attached image's framework: recover risk first, follow the trend second, and use structural breaks for the final exit.",
        "",
    ]
    for category in ("profit", "loss"):
        lines.append(f"## Top 3 {category.title()} Profiles")
        lines.append("")
        for profile in [item for item in selected if item.category == category]:
            lines.extend(
                [
                    f"### {profile.rank}. {profile.name}",
                    "",
                    f"Objective: {profile.objective}",
                    "",
                    "Rules:",
                ]
            )
            lines.extend(f"- {rule}" for rule in profile.rules)
            lines.extend(
                [
                    "",
                    f"Best for: {profile.best_for}",
                    "",
                    f"Avoid when: {profile.avoid_when}",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def _resolve_profit_profile(profile: ExitProfile | str) -> ExitProfile:
    if isinstance(profile, ExitProfile):
        if profile.category != "profit":
            raise ValueError("simulate_long_exit requires a profit profile")
        return profile
    profiles = {item.key: item for item in top_profit_taking_profiles()}
    try:
        return profiles[profile]
    except KeyError as exc:
        raise ValueError(f"unknown profit profile: {profile}") from exc


def _trailing_stop(
    rule: TrailingRule | None,
    ohlc: pd.DataFrame,
    highest_close: float,
    atr_value: float,
    entry_price: float,
    risk: float,
) -> float:
    if rule is None:
        return float("-inf")
    close = ohlc["Close"].astype(float)
    current_r = (float(close.iloc[-1]) - entry_price) / risk
    if current_r < rule.activation_r:
        return float("-inf")
    if rule.method == "chandelier" and rule.atr_multiple is not None:
        return highest_close - rule.atr_multiple * atr_value
    if rule.method == "ema" and rule.ema_period is not None:
        return float(close.ewm(span=rule.ema_period, adjust=False).mean().iloc[-1])
    if rule.method == "structure" and rule.swing_lookback is not None:
        lows = ohlc["Low"].astype(float).tail(rule.swing_lookback)
        return float(lows.min() - atr_value)
    return float("-inf")
