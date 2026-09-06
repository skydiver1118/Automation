"""Decision views derived from the production V2 scores; does not rescore stocks."""
from __future__ import annotations
import html
import json
import math
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import pandas as pd
import pandas_market_calendars as mcal

METRICS = ['buy_now_score', 'long_term_score', 'short_term_score']
TECH = ['rs_1m','rs_3m','rs_6m','rs_12m','rsi14','macd_hist','adx14','dist_20dma','dist_50dma','dist_200dma','volume_ratio_20d']
FUND = ['forward_revenue_growth','forward_eps_growth','eps_revision_signal','forward_pe','ev_sales','ev_ebitda','fcf_yield','fcf_margin','roic_proxy','gross_margin','operating_margin','debt_to_equity']
FACTORS = {'quality_score':'Quality','valuation_score':'Value','growth_score':'Growth','revision_score':'Revisions','relative_strength_score':'Relative strength','technical_score':'Technical'}

def finite(v):
    try:
        x=float(v)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError): return None

def read_json(path):
    return json.loads(path.read_text()) if path.exists() else {}

def regime(frame):
    """Require both methodology identity and the exact dated universe to match."""
    if frame.empty or 'scoring_version' not in frame: return None
    versions=frame.scoring_version.dropna().astype(str).unique()
    if len(versions)!=1 or frame.scoring_version.isna().any(): return None
    fingerprints=[]
    if 'scoring_fingerprint' in frame:
        fingerprints=frame.scoring_fingerprint.dropna().astype(str).unique().tolist()
        if frame.scoring_fingerprint.isna().any() or len(fingerprints)!=1: return None
    if frame.ticker.duplicated().any(): return None
    return (versions[0], tuple(fingerprints), tuple(sorted(frame.ticker.astype(str))))

def coverage(row):
    fields=TECH if row.get('asset_type')=='ETF' else TECH+FUND
    missing=[c for c in fields if finite(row.get(c)) is None]
    return round(100*(len(fields)-len(missing))/len(fields)), missing

def compare_snapshot(hist, date, target, metric):
    current=hist[hist.as_of==date].copy(); prior=hist[hist.as_of==target].copy()
    if prior.empty: return {}, 'Missing session'
    if regime(current) is None or regime(current)!=regime(prior): return {}, 'Method / universe reset'
    # Rank change is calculated over the complete universe, never the active UI filter.
    a=current.set_index('ticker'); b=prior.set_index('ticker')
    ar=a[metric].rank(method='min',ascending=False); br=b[metric].rank(method='min',ascending=False)
    result={}
    for t in a.index:
        x,y=finite(a.at[t,metric]),finite(b.at[t,metric])
        if x is not None and y is not None:
            result[t]={'delta':round(x-y,1),'rank_delta':int(br[t]-ar[t])}
    return result, 'Comparable'

def idea_state(row, entry):
    cov,_=coverage(row); price=finite(row.get('price'))
    lt=finite(row.get('long_term_score')); st=finite(row.get('short_term_score'))
    if cov<80 or price is None or lt is None or st is None: return 'Check data'
    if lt<55: return 'Watch only'
    if not entry: return 'Entry unavailable'
    zone=entry.get('entry_zone') or []; stop=finite(entry.get('stop_reference'))
    if stop is not None and price<=stop: return 'Setup broken'
    if len(zone)!=2 or any(finite(z) is None for z in zone): return 'Entry unavailable'
    if price<zone[0]: return 'Wait for stabilization'
    if price>zone[1]: return 'Wait for pullback'
    if st<65: return 'In zone; timing weak'
    rsi=finite(row.get('rsi14')); d50=finite(row.get('dist_50dma')); mh=finite(row.get('macd_hist'))
    if rsi is None or d50 is None or mh is None: return 'Check data'
    if rsi>=70 or d50<0 or mh<=0: return 'In zone; confirm trend'
    return 'In entry zone'

def build_payload(hist, config, canonical, entries, sessions=None):
    hist=hist.copy(); hist['as_of']=pd.to_datetime(hist.as_of).dt.strftime('%Y-%m-%d')
    hist=hist[hist.as_of!='2026-08-14'].sort_values(['as_of','ticker']).drop_duplicates(['as_of','ticker'],keep='last')
    date=hist.as_of.max(); latest=hist[hist.as_of==date].copy()
    if set(latest.ticker)!=set(config['universe']): raise ValueError('Dashboard snapshot does not match configured universe')
    if sessions is None:
        sessions=mcal.get_calendar('NYSE').schedule(start_date=pd.Timestamp(date)-pd.Timedelta(days=50),end_date=date).index.strftime('%Y-%m-%d').tolist()
    sessions=[s for s in sessions if s<=date]
    target1=sessions[-2] if len(sessions)>1 else None
    target5=sessions[-6] if len(sessions)>5 else None
    deltas={}; status={}
    for metric in METRICS:
        deltas[metric]={}
        for key,target in [('daily',target1),('weekly',target5)]:
            deltas[metric][key],status[key]=compare_snapshot(hist,date,target,metric) if target else ({},'Missing session')
    canonical_valid=canonical.get('as_of')==date
    entries_valid=entries.get('as_of')==date
    entry_map={e['ticker']:e for e in entries.get('securities',entries.get('top3',[])) if not e.get('error')} if entries_valid else {}
    latest_regime=regime(latest)
    snapshots={d:g for d,g in hist.groupby('as_of')}
    dates=sorted(snapshots)
    era={}; previous=None; era_num=0
    for d in dates:
        identity=regime(snapshots[d])
        # Unknown historical methodologies cannot be declared comparable to any other date.
        if identity is None or identity!=previous: era_num+=1
        era[d]=era_num; previous=identity
    current_era=era[date]
    records=[]
    for row in latest.to_dict('records'):
        t=row['ticker']; cov,missing=coverage(row)
        c=canonical.get('stocks',{}).get(t,{}) if canonical_valid else {}
        if c.get('as_of')!=date: c={}
        support=c.get('support',{})
        if support.get('series_as_of')!=date: support={}
        entry=entry_map.get(t,{})
        if entry.get('series_as_of',date)!=date: entry={}
        strengths=[]; risks=[]
        observed={k:finite(row.get(k)) for k in FACTORS}
        strengths=[f'{FACTORS[k]} {v:.1f}/100' for k,v in sorted(observed.items(),key=lambda kv:kv[1] if kv[1] is not None else -1,reverse=True) if v is not None and v>=60][:2]
        if not strengths: strengths=['No factor score reaches 60/100']
        if cov<100: risks.append(f'{len(missing)} inputs missing; neutral values affect scores')
        for key,label in [('fcf_yield','Negative free cash flow'),('operating_margin','Operating losses')]:
            v=finite(row.get(key))
            if v is not None and v<0: risks.append(label)
        if finite(row.get('rsi14')) is not None and row['rsi14']>=70: risks.append('RSI at or above 70')
        if finite(row.get('dist_200dma')) is not None and row['dist_200dma']>.4: risks.append('More than 40% above 200DMA')
        if finite(row.get('adx14')) is not None and row['adx14']<20: risks.append('ADX below 20; weak trend strength')
        if finite(row.get('valuation_score')) is not None and row['valuation_score']<40: risks.append('Low relative valuation score')
        if finite(row.get('operating_margin')) is not None and finite(row.get('gross_margin')) is not None and row['operating_margin']>row['gross_margin']: risks.append('Operating margin exceeds gross margin; review one-off income')
        if config.get('etf_metadata',{}).get(t,{}).get('leveraged'): risks.append('Daily leveraged ETF; compounding risk')
        if not risks: risks=['Earnings catalyst and business thesis need review']
        state=idea_state(row,entry)
        fcf=finite(row.get('fcf_yield')); op=finite(row.get('operating_margin')); quality=finite(row.get('quality_score')); val=finite(row.get('valuation_score'))
        supported=(row.get('asset_type')!='ETF' and cov>=80 and (finite(row.get('long_term_score')) or 0)>=55 and quality is not None and quality>=55 and fcf is not None and fcf>0 and op is not None and op>0)
        r={k:finite(row.get(k)) for k in METRICS+list(FACTORS)+['price','rsi14','adx14','dist_50dma','dist_200dma','fcf_yield','forward_pe','forward_revenue_growth','operating_margin']}
        r.update({'ticker':t,'asset_type':row.get('asset_type','Stock'),'name':row.get('company_name') if isinstance(row.get('company_name'),str) else t,'sector':row.get('sector') if isinstance(row.get('sector'),str) else 'Unclassified','coverage':cov,'missing':missing,'strengths':strengths,'risks':risks,'state':state,'supported':supported,'value_quality':bool(supported and quality>=60 and val is not None and val>=60),'entry':entry,'support':support.get('key_support'),'trend':c.get('technical',{}).get('trend','Unavailable'),'sentiment':c.get('diagnostic_sentiment',{}),'changes':{metric:{k:vals.get(t) for k,vals in periods.items()} for metric,periods in deltas.items()},'history':[]})
        for _,x in hist[hist.ticker==t].iterrows():
            r['history'].append({'date':x.as_of,'era':era[x.as_of],**{m:finite(x.get(m)) for m in METRICS}})
        records.append(r)
    records.sort(key=lambda r:-(r['buy_now_score'] or 0))
    for metric in METRICS:
        ranks=latest.set_index('ticker')[metric].rank(method='min',ascending=False)
        for r in records: r.setdefault('ranks',{})[metric]=int(ranks[r['ticker']]) if pd.notna(ranks[r['ticker']]) else None
    stocks=[r for r in records if r['asset_type']!='ETF']
    breadth_rows=[r for r in stocks if r['dist_50dma'] is not None]
    above=sum(r['dist_50dma']>0 for r in breadth_rows)
    return {'schema_version':1,'as_of':date,'created_at':datetime.now(ZoneInfo('America/New_York')).strftime('%b %d, %Y %I:%M %p %Z'),'scoring_version':latest.scoring_version.iloc[0] if 'scoring_version' in latest else 'Unknown','current_era':current_era,'era_start':min(d for d in dates if era[d]==current_era),'dates':dates,'targets':{'daily':target1,'weekly':target5},'comparison_status':status,'records':records,'breadth':{'above_50dma':above,'observed':len(breadth_rows),'stock_count':len(stocks)},'image_mentions':config.get('image_mentions',{}),'data_sources':{'prices':'Yahoo Finance adjusted daily OHLCV via yfinance','fundamentals':'Yahoo Finance company fundamentals and analyst estimates via yfinance','support':'Daily OHLCV: moving averages, swing lows, Fibonacci and ATR'}}

def render_main(hist,config,root,out):
    payload=build_payload(hist,config,read_json(root/'canonical_market.json'),read_json(root/'entry_analysis.json'))
    out.mkdir(exist_ok=True)
    for name in ['investment-dashboard.js','investment-dashboard.css']:
        shutil.copy2(root/'assets'/name,out/name)
    (out/'investment-data.json').write_text(json.dumps(payload,indent=2,allow_nan=False))
    (out/'latest_scores.csv').write_bytes((root/'latest_scores.csv').read_bytes())
    encoded=json.dumps(payload,allow_nan=False).replace('<','\\u003c')
    page=(root/'assets'/'investment-dashboard.html').read_text().replace('__DATA__',encoded)
    (out/'index.html').write_text(page)
    print(f'Investment dashboard: {len(payload["records"])} securities; comparisons {payload["comparison_status"]}')
