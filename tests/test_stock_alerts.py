import pandas as pd

from src.strategy_lab.stock_alerts import AlertRule, evaluate_rule


def make_history(values: list[float]) -> pd.DataFrame:
    index = pd.date_range("2026-01-01", periods=len(values), freq="D")
    return pd.DataFrame({"Close": values}, index=index)


def test_below_sma_triggers_when_last_close_is_below_average() -> None:
    rule = AlertRule(symbol="QQQ", condition="below_sma", window=3)
    state = {"rules": {}}
    data = make_history([10, 10, 10, 10, 8])

    result = evaluate_rule(rule, data, state)

    assert result.triggered is True
    assert result.should_notify is True
    assert result.price == 8
    assert round(result.sma, 4) == 9.3333


def test_enter_notification_only_fires_once_while_active() -> None:
    rule = AlertRule(symbol="QQQ", condition="below_sma", window=3)
    state = {"rules": {}}
    data = make_history([10, 10, 10, 10, 8])

    first = evaluate_rule(rule, data, state)
    second = evaluate_rule(rule, data, state)

    assert first.should_notify is True
    assert second.should_notify is False


def test_cross_below_sma_requires_a_new_cross() -> None:
    rule = AlertRule(symbol="QQQ", condition="cross_below_sma", window=3)
    state = {"rules": {}}
    data = make_history([10, 10, 10, 11, 8])

    result = evaluate_rule(rule, data, state)

    assert result.triggered is True
    assert result.should_notify is True
