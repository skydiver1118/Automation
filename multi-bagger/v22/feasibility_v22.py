#!/usr/bin/env python3
"""v2.2 scenario arithmetic; diagnostic only, never a probability or rank engine.

Equity P/E is applied to earnings attributable to common equity AFTER interest
and tax. Net debt is therefore not subtracted again. An explicit enterprise
EBITDA model is provided for enterprise-valued scenarios and bridges all claims.
"""
from __future__ import annotations
import math

VERSION = '2.2.1'
METHODOLOGY = 'MB_5X_FEASIBILITY_SHADOW_V2_2'
ANCHORS_X = [1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.0]
ANCHORS_Y = [0.0, 15.0, 30.0, 50.0, 70.0, 85.0, 100.0]

def _finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)

def _interp(x):
    if not _finite(x):
        return None
    if x <= ANCHORS_X[0]:
        return ANCHORS_Y[0]
    if x >= ANCHORS_X[-1]:
        return ANCHORS_Y[-1]
    for x0, x1, y0, y1 in zip(ANCHORS_X[:-1], ANCHORS_X[1:], ANCHORS_Y[:-1], ANCHORS_Y[1:]):
        if x <= x1:
            return y0 + (x-x0)*(y1-y0)/(x1-x0)
    raise AssertionError('Unreachable interval')

def _validate(market_cap, revenue_ttm, revenue_cagr, margin, multiple, dilution):
    if not all(_finite(v) for v in (market_cap, revenue_ttm, revenue_cagr, margin, multiple, dilution)):
        raise ValueError('Every input must be finite; missing is not zero')
    if market_cap <= 0 or revenue_ttm <= 0 or revenue_cagr <= -1 or multiple <= 0 or dilution <= -1:
        raise ValueError('Invalid capitalization, revenue, growth, multiple or dilution')
    if not 0 <= margin <= 1:
        raise ValueError('Normalized nonnegative margin must be a fraction between zero and one')

def _result(market_cap, revenue_ttm, revenue_cagr, dilution, equity, **details):
    revenue5 = revenue_ttm * (1 + revenue_cagr)**5
    if not all(_finite(v) for v in (revenue5, equity)):
        raise ValueError('Scenario overflow')
    equity = max(0., equity)
    equivalent = equity/(1 + dilution)
    multiple = equivalent/market_cap
    required = market_cap * 5 * (1 + dilution)
    if not all(_finite(v) for v in (equivalent, multiple, required, market_cap*5)):
        raise ValueError('Derived capitalization or per-share multiple overflow')
    return {
        'current_market_cap': market_cap,
        'required_5x_market_cap': market_cap*5,
        'incremental_equity_value_required': market_cap*4,
        'required_5x_market_cap_dilution_adjusted': required,
        'incremental_equity_value_required_dilution_adjusted': required-market_cap,
        'revenue_ttm': revenue_ttm, 'revenue_cagr': revenue_cagr, 'revenue_5y': revenue5,
        'dilution_5y': dilution, 'terminal_equity_value_5y': equity,
        # This is a current-share-equivalent value, NOT the future company's market cap.
        'supportable_equity_value_5y': equivalent,
        'supportable_current_share_equivalent_equity_value': equivalent,
        'supportable_5y_multiple': multiple, 'feasibility_gap': multiple/5,
        'shadow_feasibility_score': _interp(multiple),
        'calibrated_probability_5x': None, 'final_multibagger_score': None,
        'status': 'shadow_uncalibrated', 'engine_version': VERSION,
        'horizon_years': 5, 'return_basis': 'terminal_share_price_multiple_excluding_dividends',
        **details,
    }

def scenario(*, market_cap, revenue_ttm, revenue_cagr, net_margin, terminal_pe,
             dilution_5y=0., net_debt_5y=0.):
    """Equity P/E route. Nonzero net_debt is rejected to prevent double subtraction.

    API default zero dilution is for backward-compatible arithmetic calls only.
    Production scenario records require an EXPLICIT evidenced dilution assumption.
    """
    _validate(market_cap, revenue_ttm, revenue_cagr, net_margin, terminal_pe, dilution_5y)
    if not _finite(net_debt_5y) or net_debt_5y != 0:
        raise ValueError('P/E already values equity. Use enterprise_scenario for a net-debt bridge.')
    equity = revenue_ttm * (1+revenue_cagr)**5 * net_margin * terminal_pe
    return _result(market_cap, revenue_ttm, revenue_cagr, dilution_5y, equity,
                   model='equity_pe', normalized_net_margin=net_margin, terminal_pe=terminal_pe)

def enterprise_scenario(*, market_cap, revenue_ttm, revenue_cagr, ebitda_margin,
                        terminal_ev_ebitda, dilution_5y, net_debt_5y,
                        preferred_claims_5y, minority_claims_5y, other_claims_5y):
    """Enterprise route; all claims must be explicit, including documented zeros.

    Net debt may be negative (net cash); non-common claims cannot be negative.
    This is not a reactor/project valuation or a substitute for a funding analysis.
    """
    _validate(market_cap, revenue_ttm, revenue_cagr, ebitda_margin, terminal_ev_ebitda, dilution_5y)
    claims = (net_debt_5y, preferred_claims_5y, minority_claims_5y, other_claims_5y)
    if not all(_finite(v) for v in claims) or any(v < 0 for v in claims[1:]):
        raise ValueError('Every enterprise-to-equity capital claim must be explicit and valid')
    ev = revenue_ttm*(1+revenue_cagr)**5*ebitda_margin*terminal_ev_ebitda
    return _result(market_cap, revenue_ttm, revenue_cagr, dilution_5y, ev-sum(claims),
                   model='enterprise_ebitda', terminal_enterprise_value_5y=ev,
                   normalized_ebitda_margin=ebitda_margin, terminal_ev_ebitda=terminal_ev_ebitda,
                   net_debt_5y=net_debt_5y, preferred_claims_5y=preferred_claims_5y,
                   minority_claims_5y=minority_claims_5y, other_claims_5y=other_claims_5y)

def scenario_set(*, market_cap, revenue_ttm, bear, base, bull, model='equity_pe'):
    fn = {'equity_pe': scenario, 'enterprise_ebitda': enterprise_scenario}.get(model)
    if fn is None:
        raise ValueError('Unsupported sector model; retain Research Hold')
    out = {name: fn(market_cap=market_cap, revenue_ttm=revenue_ttm, **args)
           for name, args in [('bear', bear), ('base', base), ('bull', bull)]}
    multiples = [out[n]['supportable_5y_multiple'] for n in ('bear', 'base', 'bull')]
    if multiples != sorted(multiples):
        raise ValueError('Bear/base/bull outcomes are not ordered; review assumptions')
    return {'methodology': METHODOLOGY, 'production_rank_effect': False,
            'scenarios': out, 'shadow_score': out['base']['shadow_feasibility_score'],
            'calibrated_probability_5x': None, 'final_multibagger_score': None}

def reverse_requirements(*, market_cap, revenue_ttm, dilution_5y, net_margin, terminal_pe):
    """What MUST happen at explicitly hypothetical economics, not what WILL happen."""
    _validate(market_cap, 1 if revenue_ttm is None else revenue_ttm, 0,
              net_margin, terminal_pe, dilution_5y)
    if net_margin == 0:
        raise ValueError('A positive earnings margin is required for this reverse bridge')
    equity = 5*market_cap*(1+dilution_5y)
    income = equity/terminal_pe
    revenue = income/net_margin
    cagr = (revenue/revenue_ttm)**.2-1 if revenue_ttm is not None else None
    if not all(_finite(v) for v in (equity, income, revenue)) or cagr is not None and not _finite(cagr):
        raise ValueError('Reverse-hurdle calculation overflow')
    return {'dilution_5y': dilution_5y, 'net_margin': net_margin, 'terminal_pe': terminal_pe,
            'required_terminal_equity': equity, 'required_common_net_income': income,
            'required_revenue': revenue,
            'required_revenue_cagr': cagr,
            'status': 'hypothetical_reverse_requirements_not_forecast',
            'horizon_years': 5, 'probability_5x': None}
