#!/usr/bin/env python3
"""Uncalibrated v2.2 5x-feasibility shadow layer.

This module does NOT alter the frozen v2.1 production score. It exposes auditable
scenario math for validation until a point-in-time historical calibration dataset exists.
"""
from __future__ import annotations
import math

ANCHORS_X=[1.0,1.5,2.0,3.0,4.0,5.0,7.0]
ANCHORS_Y=[0.0,15.0,30.0,50.0,70.0,85.0,100.0]

def _finite(x):
    return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(float(x))

def _interp(x):
    if not _finite(x): return None
    if x<=ANCHORS_X[0]: return ANCHORS_Y[0]
    if x>=ANCHORS_X[-1]: return ANCHORS_Y[-1]
    for x0,x1,y0,y1 in zip(ANCHORS_X[:-1],ANCHORS_X[1:],ANCHORS_Y[:-1],ANCHORS_Y[1:]):
        if x<=x1:
            return y0+(x-x0)*(y1-y0)/(x1-x0)
    raise AssertionError("unreachable")

def scenario(*, market_cap, revenue_ttm, revenue_cagr, net_margin, terminal_pe,
             dilution_5y=0.0, net_debt_5y=0.0):
    """Return transparent 5-year equity-value feasibility math.

    dilution_5y is cumulative fractional share-count growth over five years. The
    supportable multiple is adjusted per current share by dividing by 1+dilution.
    net_debt_5y is subtracted from terminal equity value only when the scenario
    was built from enterprise economics that require it; default is zero.
    """
    vals=[market_cap,revenue_ttm,revenue_cagr,net_margin,terminal_pe,dilution_5y,net_debt_5y]
    if not all(_finite(v) for v in vals): raise ValueError("All scenario inputs must be finite")
    if market_cap<=0 or revenue_ttm<=0 or terminal_pe<=0 or dilution_5y<=-1:
        raise ValueError("Invalid positive-value or dilution input")
    revenue_5=revenue_ttm*((1+revenue_cagr)**5)
    earnings_5=revenue_5*net_margin
    raw_equity=max(0.0,earnings_5*terminal_pe-net_debt_5y)
    per_current_share_equity=raw_equity/(1+dilution_5y)
    multiple=per_current_share_equity/market_cap
    return {
        "current_market_cap":market_cap,
        "required_5x_market_cap":market_cap*5,
        "incremental_equity_value_required":market_cap*4,
        "revenue_ttm":revenue_ttm,
        "revenue_cagr":revenue_cagr,
        "revenue_5y":revenue_5,
        "normalized_net_margin":net_margin,
        "terminal_pe":terminal_pe,
        "dilution_5y":dilution_5y,
        "supportable_equity_value_5y":per_current_share_equity,
        "supportable_5y_multiple":multiple,
        "feasibility_gap":multiple/5,
        "shadow_feasibility_score":_interp(multiple),
        "calibrated_probability_5x":None,
        "status":"shadow_uncalibrated",
    }

def scenario_set(*, market_cap, revenue_ttm, bear, base, bull):
    out={}
    for name,args in [("bear",bear),("base",base),("bull",bull)]:
        out[name]=scenario(market_cap=market_cap,revenue_ttm=revenue_ttm,**args)
    return {"methodology":"MB_5X_FEASIBILITY_SHADOW_V2_2","production_rank_effect":False,
            "scenarios":out,"shadow_score":out["base"]["shadow_feasibility_score"]}
