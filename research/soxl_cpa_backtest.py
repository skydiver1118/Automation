from __future__ import annotations
import json, math, pathlib
import numpy as np
import pandas as pd

OUT = pathlib.Path('artifacts/soxl_cpa')
OUT.mkdir(parents=True, exist_ok=True)
COST = 0.0005  # 5 bps per transaction side


def load_data():
    # Prefer Yahoo via yfinance for freshest adjusted OHLCV; fall back to public snapshot.
    try:
        import yfinance as yf
        d = yf.download('SOXL', start='2010-03-01', auto_adjust=True, progress=False, actions=False)
        if isinstance(d.columns, pd.MultiIndex): d.columns = d.columns.get_level_values(0)
        d = d[['Open','High','Low','Close','Volume']].dropna().copy()
        if len(d) > 3000:
            d.index = pd.to_datetime(d.index).tz_localize(None)
            return d, 'Yahoo Finance via yfinance (auto-adjusted)'
    except Exception:
        pass
    url='https://raw.githubusercontent.com/awakzdev/finance-data/refs/heads/main/soxl_stock_data.csv'
    d=pd.read_csv(url)
    d['Date']=pd.to_datetime(d['Date'], dayfirst=True)
    d=d.set_index('Date').sort_index()
    d=d[['Open','High','Low','Close','Volume']].dropna()
    return d, url


def indicators(d):
    x=d.copy()
    x['ema10']=x.Close.ewm(span=10,adjust=False).mean()
    x['ema20']=x.Close.ewm(span=20,adjust=False).mean()
    x['sma50']=x.Close.rolling(50).mean()
    x['sma200']=x.Close.rolling(200).mean()
    x['spread']=(x.ema10-x.ema20).abs()/x.Close
    x['spread5']=x.spread.rolling(5).mean()
    x['volmed20']=x.Volume.rolling(20).median()
    x['hh5']=x.High.shift(1).rolling(5).max()
    prevmax=np.maximum(x.ema10.shift(1),x.ema20.shift(1))
    wedge=(x.Close>x.ema10)&(x.Close>x.ema20)&(x.Close.shift(1)<=prevmax)&(x.Close>x.hh5)&(x.spread<x.spread5)&(x.Volume>x.volmed20)
    touch=(x.Low<=x.ema10)&(x.Low>=x.ema20*0.97)
    cross=(x.ema10>x.ema20)&touch&(x.Close>x.ema10)&(x.Close>x.Close.shift(1))
    x['entry_base']=wedge|cross
    return x


def make_signal(x, variant):
    entry=x.entry_base.copy()
    if variant=='Regime':
        entry &= (x.Close>x.sma50)&(x.sma50>x.sma200)&(x.ema10>x.ema20)
    if variant=='Core': exit_sig=(x.Close<x.ema10)&(x.Close<x.ema20)
    elif variant=='Fast': exit_sig=(x.Close<x.ema10)
    else: exit_sig=((x.Close<x.ema20)|(x.Close<x.sma50))
    desired=np.zeros(len(x),dtype=int); state=0
    for i in range(len(x)):
        if state==0 and bool(entry.iloc[i]): state=1
        elif state==1 and bool(exit_sig.iloc[i]): state=0
        desired[i]=state
    # signal at close t executes at open t+1
    pos=pd.Series(desired,index=x.index).shift(1).fillna(0).astype(int)
    return pos


def backtest(x, variant):
    pos=make_signal(x,variant)
    op=x.Open.astype(float)
    r=op.shift(-1)/op-1
    r.iloc[-1]=x.Close.iloc[-1]/op.iloc[-1]-1
    strat=pos*r
    changes=pos.diff().abs().fillna(pos.abs())
    strat -= changes*COST
    eq=(1+strat.fillna(0)).cumprod()
    # trades from position transitions, executed at opens
    trades=[]; entry_i=None; entry_px=None
    for i in range(len(x)):
        if i>0 and pos.iloc[i]==1 and pos.iloc[i-1]==0:
            entry_i=i; entry_px=op.iloc[i]*(1+COST)
        if i>0 and pos.iloc[i]==0 and pos.iloc[i-1]==1 and entry_i is not None:
            exit_px=op.iloc[i]*(1-COST); ret=exit_px/entry_px-1
            trades.append((x.index[entry_i],x.index[i],entry_px,exit_px,ret)); entry_i=None
    if entry_i is not None:
        exit_px=x.Close.iloc[-1]*(1-COST); ret=exit_px/entry_px-1
        trades.append((x.index[entry_i],x.index[-1],entry_px,exit_px,ret))
    return strat,eq,pos,trades


def stats(r,eq,pos,trades,start,end):
    yrs=(end-start).days/365.2425
    total=eq.iloc[-1]-1; cagr=eq.iloc[-1]**(1/yrs)-1
    dd=eq/eq.cummax()-1; mdd=dd.min()
    ann=math.sqrt(252); sd=r.std(ddof=0); sharpe=(r.mean()/sd*ann) if sd>0 else np.nan
    dn=r[r<0].std(ddof=0); sortino=(r.mean()/dn*ann) if dn>0 else np.nan
    calmar=cagr/abs(mdd) if mdd<0 else np.nan
    tr=np.array([t[4] for t in trades],float); wins=tr[tr>0]; losses=tr[tr<=0]
    pf=wins.sum()/abs(losses.sum()) if len(losses) and losses.sum()!=0 else np.nan
    return {'total_return':total,'CAGR':cagr,'max_drawdown':mdd,'Sharpe':sharpe,'Sortino':sortino,'Calmar':calmar,'trades':len(trades),'win_rate':float((tr>0).mean()) if len(tr) else np.nan,'avg_winner':wins.mean() if len(wins) else np.nan,'avg_loser':losses.mean() if len(losses) else np.nan,'profit_factor':pf,'exposure':pos.mean(),'worst_trade':tr.min() if len(tr) else np.nan}


def stress(eq, idx, start, end):
    s=eq[(idx>=pd.Timestamp(start))&(idx<=pd.Timestamp(end))]
    return float((s/s.cummax()-1).min()) if len(s) else np.nan


d,source=load_data(); x=indicators(d).dropna().copy()
results={}; trade_rows=[]
for v in ['Core','Fast','Regime']:
    r,eq,pos,trades=backtest(x,v); m=stats(r,eq,pos,trades,x.index[0],x.index[-1]);
    m['2020_crash_dd']=stress(eq,x.index,'2020-02-19','2020-03-23'); m['2022_bear_dd']=stress(eq,x.index,'2022-01-03','2022-10-14'); results[v]=m
    for a,b,ep,xp,tr in trades: trade_rows.append({'variant':v,'entry':a.date().isoformat(),'exit':b.date().isoformat(),'entry_price':ep,'exit_price':xp,'return':tr})
# Buy & hold from common post-warmup start
bh_ret=x.Open.shift(-1)/x.Open-1; bh_ret.iloc[-1]=x.Close.iloc[-1]/x.Open.iloc[-1]-1
bh_eq=(1+bh_ret.fillna(0)).cumprod(); bh_pos=pd.Series(1,index=x.index)
results['BuyHold']=stats(bh_ret,bh_eq,bh_pos,[],x.index[0],x.index[-1]); results['BuyHold']['trades']=1; results['BuyHold']['win_rate']=np.nan; results['BuyHold']['avg_winner']=np.nan; results['BuyHold']['avg_loser']=np.nan; results['BuyHold']['profit_factor']=np.nan; results['BuyHold']['worst_trade']=np.nan; results['BuyHold']['2020_crash_dd']=stress(bh_eq,x.index,'2020-02-19','2020-03-23'); results['BuyHold']['2022_bear_dd']=stress(bh_eq,x.index,'2022-01-03','2022-10-14')
meta={'source':source,'rows':len(x),'start':x.index[0].date().isoformat(),'end':x.index[-1].date().isoformat(),'cost_per_side':COST,'execution':'signals at close, trades next open'}
with open(OUT/'results.json','w') as f: json.dump({'meta':meta,'results':results},f,indent=2,default=float)
pd.DataFrame(trade_rows).to_csv(OUT/'trades.csv',index=False)
rows=[]
for k,v in results.items():
    rows.append([k,v['CAGR'],v['total_return'],v['max_drawdown'],v['Sharpe'],v['Sortino'],v['Calmar'],v['trades'],v['win_rate'],v['profit_factor'],v['exposure'],v['2020_crash_dd'],v['2022_bear_dd']])
tab=pd.DataFrame(rows,columns=['Strategy','CAGR','TotalReturn','MaxDD','Sharpe','Sortino','Calmar','Trades','WinRate','ProfitFactor','Exposure','2020DD','2022DD'])
tab.to_csv(OUT/'summary.csv',index=False)
print(json.dumps({'meta':meta,'results':results},indent=2,default=float))
