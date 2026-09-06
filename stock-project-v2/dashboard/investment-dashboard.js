(() => {
'use strict';
const data=JSON.parse(document.getElementById('investment-data').textContent), rows=data.records;
const el=id=>document.getElementById(id), esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const number=(v,d=1)=>v==null?'—':Number(v).toFixed(d), money=v=>v==null?'—':new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(v);
const capitalization=v=>v==null?'—':new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',notation:'compact',maximumFractionDigits:2}).format(v);
const setupLabel=r=>r.state==='In zone; timing weak'?'Within entry band; timing remains weak':r.state;
const entryBand=r=>r.entry.entry_zone?.length===2?r.entry.entry_zone.map(money).join('–'):'Unavailable';
const sign=v=>v==null?'—':`${v>0?'+':''}${number(v)}`, color=v=>v==null?'neutral':v>0?'positive':v<0?'negative':'neutral';
let ideaMode='supported';
const metric=()=>el('metric').value;
const change=(r,period)=>r.changes[metric()][period];
const weekly=r=>r.changes.buy_now_score.weekly?.delta;
const rules={supported:'Stocks only · Long-term ≥55 · Quality ≥55 · Positive FCF and operating margin · Observed inputs ≥80% · Ordered by composite score.',value:'Best-supported stocks with quality ≥60 and valuation ≥60. A relative value score is not a fair-value price target.',improving:'Best-supported stocks with a positive composite change over five comparable NYSE sessions. Method changes and missing sessions are excluded.',etf:'ETF scores use their existing price/momentum framework. Corporate profitability filters do not apply; daily leverage is flagged.'};
el('timestamp').innerHTML=`Last completed session <strong>${esc(data.as_of)}</strong><small>Generated ${esc(data.created_at)}</small>`;
const supported=rows.filter(r=>r.supported),ready=supported.filter(r=>r.state==='In entry zone'),pullbacks=supported.filter(r=>r.state==='Wait for pullback');
el('summary').innerHTML=[['Best-supported stocks',supported.length,'Profitability + quality screen'],['In entry zone',ready.length,'Among best-supported stocks'],['Waiting for pullback',pullbacks.length,'Among best-supported stocks'],['Watchlist breadth',`${data.breadth.above_50dma}/${data.breadth.observed}`,'Stocks above 50DMA · observed inputs only']].map(([a,b,c])=>`<div><span>${a}</span><strong>${b}</strong><span>${c}</span></div>`).join('');
function renderSetups(){
 const order=['In entry zone','In zone; timing weak','In zone; confirm trend','Wait for pullback','Wait for stabilization','Setup broken','Check data','Entry unavailable','Watch only'];
 const states=[...new Set(supported.map(r=>r.state))].sort((a,b)=>order.indexOf(a)-order.indexOf(b));
 el('setup-groups').innerHTML=states.map(state=>{const list=supported.filter(r=>r.state===state);return `<article class="setup-group ${state==='In entry zone'?'ready':''}"><h3>${esc(setupLabel(list[0]))} · ${list.length}</h3><ul>${list.map(r=>`<li><a class="ticker" href="stocks/${esc(r.ticker)}.html">${esc(r.ticker)}</a><span>Close <strong>${money(r.price)}</strong> · Entry band <strong>${entryBand(r)}</strong><br>Short-term / entry score <strong>${number(r.short_term_score)}/100</strong></span></li>`).join('')}</ul></article>`;}).join('')||'<p class="muted">No stocks currently pass the best-supported screen.</p>';
}
function ideaCard(r){
 const e=r.entry,z=e.entry_zone,stop=e.stop_reference;
 const zone=z?.length===2?`${money(z[0])}–${money(z[1])}`:'Unavailable';
 const gap=z?.length===2&&r.price>z[1]?`${number((z[1]/r.price-1)*100)}% to zone top`:'';
 const risk=stop!=null&&r.price>stop?`${number((r.price-stop)/r.price*100)}% below price`:'Reference unavailable';
 return `<article class="idea"><div class="idea-head"><div><h3><a href="stocks/${esc(r.ticker)}.html">${esc(r.ticker)}</a></h3><div class="company">${esc(r.name)} · ${esc(r.sector)} <span class="badge">${esc(r.asset_type)}</span></div></div><div class="score-large">${number(r.buy_now_score)}<small>COMPOSITE / 100</small></div></div><span class="pill ${r.state==='In entry zone'?'ready':''}">${esc(setupLabel(r))}</span><dl><div><dt>Long-term / Entry</dt><dd>${number(r.long_term_score)} / ${number(r.short_term_score)}</dd></div><div><dt>Observed inputs</dt><dd>${r.coverage}%</dd></div><div><dt>Latest close</dt><dd>${money(r.price)}</dd></div><div><dt>Support entry band</dt><dd>${zone}</dd><dt>${esc(gap)}</dt></div><div><dt>Breakout reference</dt><dd>${money(e.breakout_trigger)}</dd></div><div><dt>Stop reference</dt><dd>${money(stop)}</dd><dt>${risk}</dt></div></dl><div class="evidence"><b>Why it screens well</b>${esc(r.strengths.join(' · '))}<b>What needs attention</b>${esc(r.risks.slice(0,3).join(' · '))}</div><a class="more" href="stocks/${esc(r.ticker)}.html">Review full diagnostics →</a></article>`;
}
function renderIdeas(){
 let list=rows.filter(r=>ideaMode==='supported'?r.supported:ideaMode==='value'?r.value_quality:ideaMode==='improving'?r.supported&&weekly(r)>0:r.asset_type==='ETF');
 if(ideaMode==='improving')list.sort((a,b)=>weekly(b)-weekly(a));
 el('screen-rule').textContent=rules[ideaMode];
 el('idea-cards').innerHTML=list.length?list.slice(0,3).map(ideaCard).join(''):`<div class="empty">${ideaMode==='improving'&&data.comparison_status.weekly!=='Comparable'?'Waiting for five comparable sessions. No improvement is inferred across the recent reset.':'No securities currently pass this screen. The dashboard will not force a recommendation.'}</div>`;
 el('idea-tabs').querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===ideaMode)));
}
el('idea-tabs').addEventListener('click',e=>{const b=e.target.closest('button[data-mode]');if(b){ideaMode=b.dataset.mode;renderIdeas();}});
const sectors=[...new Set(rows.map(r=>r.sector))].sort();
el('sector').innerHTML='<option value="all">All sectors</option>'+sectors.map(s=>`<option>${esc(s)}</option>`).join('');
function spark(r){
 const points=r.history.slice(-20),m=metric(),width=118,height=36,pad=3;
 const valid=points.filter(p=>p[m]!=null);
 if(!valid.length)return '<span class="neutral">No history</span>';
 const coords=points.map((p,i)=>({x:pad+i*(width-2*pad)/Math.max(points.length-1,1),y:height-pad-(p[m]??0)/100*(height-2*pad),...p}));
 let svg='';coords.forEach((p,i)=>{if(p[m]==null)return;const prev=coords[i-1];const c=p.era===data.current_era?'#82bbff':'#637f9b';if(prev&&prev[m]!=null&&prev.era===p.era)svg+=`<line x1="${prev.x}" y1="${prev.y}" x2="${p.x}" y2="${p.y}" stroke="${c}" stroke-width="1.8"/>`;svg+=`<circle cx="${p.x}" cy="${p.y}" r="2" fill="${c}"><title>${esc(p.date)}: ${number(p[m])}</title></circle>`;});
 return `<svg class="spark" viewBox="0 0 ${width} ${height}" role="img" aria-label="${esc(r.ticker)} score history on a zero to one hundred scale; breaks indicate resets">${svg}</svg>`;
}
function deltaCell(r,period){const d=change(r,period);return d?`<span class="num ${color(d.delta)}">${sign(d.delta)}</span>`:`<span class="neutral">—</span><small>${esc(data.comparison_status[period])}</small>`;}
function sentimentPercentages(r){
 const s=r.sentiment,c=s?.counts;
 const directional=c?(c.bullish??0)+(c.favorable??0)+(c.bearish??0):0;
 const bullish=directional>0&&Number.isFinite(s.positive_pct)?s.positive_pct:null;
 return {bullish,bearish:bullish==null?null:100-bullish};
}
function filteredRows(){
 const term=el('search').value.trim().toLowerCase(),asset=el('asset-type').value,sector=el('sector').value,focus=el('focus').value,sort=el('sort').value;
 let result=rows.filter(r=>(!term||`${r.ticker} ${r.name}`.toLowerCase().includes(term))&&(asset==='all'||r.asset_type===asset)&&(sector==='all'||r.sector===sector)&&(focus==='all'||focus==='supported'&&r.supported||focus==='timing-weak'&&r.state==='In zone; timing weak'||focus==='improving'&&(change(r,'weekly')?.delta??0)>0||focus==='declining'&&(change(r,'weekly')?.delta??0)<0||focus==='data'&&r.coverage<100));
 const value=r=>sort==='daily'?change(r,'daily')?.delta:sort==='rank'?change(r,'weekly')?.rank_delta:['weekly','decline'].includes(sort)?change(r,'weekly')?.delta:r[metric()];
 result.sort((a,b)=>{if(sort==='ticker')return a.ticker.localeCompare(b.ticker);const x=value(a),y=value(b);if(x==null&&y!=null)return 1;if(y==null&&x!=null)return -1;return (x!=null&&y!=null?(sort==='decline'?x-y:y-x):0)||(b[metric()]??-1)-(a[metric()]??-1)||a.ticker.localeCompare(b.ticker);});
 return result;
}
function renderTracker(){
 const list=filteredRows(),m=metric();
 el('comparison-note').textContent=`1 session: ${data.targets.daily??'unavailable'} → ${data.as_of} (${data.comparison_status.daily}). 5 sessions: ${data.targets.weekly??'unavailable'} → ${data.as_of} (${data.comparison_status.weekly}). Comparable baseline begins ${data.era_start}.`;
 el('row-count').textContent=`${list.length} of ${rows.length} securities · Ranks always use the full ${rows.length}-security universe.${data.comparison_status.weekly!=='Comparable'&&['weekly','decline','rank'].includes(el('sort').value)?' Weekly changes unavailable; sorted by current score.':''}`;
 const scoreCell=(r,key)=>`<span class="num">${number(r[key])}</span>${r.ranks[key]!=null?`<small>Rank ${r.ranks[key]}</small>`:''}`;
 el('tracker-rows').innerHTML=list.map(r=>{
  const d=change(r,'weekly'), percentages=sentimentPercentages(r);
  const sentiment=r.sentiment?.label?`${esc(r.sentiment.label)}<small>${number(r.sentiment.positive_pct,0)}% bullish indicators</small>`:'—';
  const cells=[
   `<a class="ticker" href="stocks/${esc(r.ticker)}.html" title="${esc(r.name)}">${esc(r.ticker)}</a><small>${esc(r.sector)}</small>`,
   r.ranks[m]??'—',esc(r.asset_type),money(r.price),capitalization(r.market_cap),
   ...['long_term_score','short_term_score','buy_now_score'].map(key=>scoreCell(r,key)),
   ...['bullish','bearish'].map(key=>percentages[key]==null?'<span class="neutral">—</span>':`<span class="num ${key==='bullish'?'positive':'negative'}">${number(percentages[key],0)}%</span>`),
   ...['valuation_score','quality_score','growth_score','revision_score','relative_strength_score','technical_score'].map(key=>scoreCell(r,key)),
   number(r.rsi14),sentiment,
   `<span class="${r.state==='In entry zone'?'positive':''}">${esc(setupLabel(r))}</span>`,entryBand(r),
   `<span title="${esc(r.missing.join(', '))}">${r.coverage}%</span>${r.missing.length?`<small>${r.missing.length} missing</small>`:''}`,
   deltaCell(r,'daily'),deltaCell(r,'weekly'),
   d?`<span class="${color(d.rank_delta)}">${d.rank_delta>0?'↑ '+d.rank_delta:d.rank_delta<0?'↓ '+Math.abs(d.rank_delta):'Unchanged'}</span>`:'<span class="neutral">—</span>',
   spark(r)
  ];
  return `<tr>${cells.map(cell=>`<td>${cell}</td>`).join('')}</tr>`;
 }).join('')||'<tr><td colspan="25">No securities match these filters.</td></tr>';
}
const colors=['#82bbff','#67dfb1','#ffd18a'];
for(let i=1;i<=3;i++){el(`compare-${i}`).innerHTML='<option value="">None</option>'+rows.map(r=>`<option value="${esc(r.ticker)}">${esc(r.ticker)}</option>`).join('');el(`compare-${i}`).value=(supported[i-1]||rows[i-1])?.ticker??'';el(`compare-${i}`).addEventListener('change',renderComparison);}
function renderComparison(){
 const tickers=[...new Set([1,2,3].map(i=>el(`compare-${i}`).value).filter(Boolean))], m=metric(),all=el('history-mode').value==='all';
 const dates=data.dates.filter(d=>all||d>=data.era_start),w=1000,h=300,pad={l:44,r:20,t:15,b:42};
 const x=d=>pad.l+dates.indexOf(d)*(w-pad.l-pad.r)/Math.max(dates.length-1,1),y=v=>h-pad.b-v/100*(h-pad.b-pad.t);
 let svg='';for(const v of [0,25,50,75,100])svg+=`<line x1="${pad.l}" x2="${w-pad.r}" y1="${y(v)}" y2="${y(v)}" stroke="#294158"/><text x="${pad.l-10}" y="${y(v)+4}" text-anchor="end" fill="#a4b7ca" font-size="12">${v}</text>`;
 const labels=[...new Set([0,Math.floor((dates.length-1)/3),Math.floor((dates.length-1)*2/3),dates.length-1])];
 labels.forEach(i=>{if(dates[i])svg+=`<text x="${x(dates[i])}" y="${h-13}" text-anchor="${i===0?'start':i===dates.length-1?'end':'middle'}" fill="#a4b7ca" font-size="12">${esc(dates[i])}</text>`;});
 tickers.forEach((t,i)=>{const r=rows.find(r=>r.ticker===t),points=r.history.filter(p=>dates.includes(p.date));points.forEach((p,j)=>{if(p[m]==null)return;const prev=points[j-1];if(prev&&prev[m]!=null&&prev.era===p.era)svg+=`<line x1="${x(prev.date)}" y1="${y(prev[m])}" x2="${x(p.date)}" y2="${y(p[m])}" stroke="${colors[i]}" stroke-width="2.5"/>`;svg+=`<circle cx="${x(p.date)}" cy="${y(p[m])}" r="4" fill="${colors[i]}"><title>${esc(t)} · ${esc(p.date)} · ${number(p[m])}</title></circle>`;});});
 el('compare-legend').innerHTML=tickers.map((t,i)=>`<span><i style="background:${colors[i]}"></i>${esc(t)}</span>`).join('');
 el('compare-chart').innerHTML=tickers.length?`<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(tickers.join(', '))} score comparison; zero to one hundred scale">${svg}</svg>`:'<div class="empty">Select up to three securities to compare.</div>';
 el('chart-note').textContent=`${dates.length} saved session${dates.length===1?'':'s'} in this view. ${dates.length<2?'Only the baseline is available; a trend needs another comparable session. ':''}Lines never connect different methods or universes. Older unverified snapshots are isolated points.`;
}
for(const id of ['metric','asset-type','sector','focus','sort'])el(id).addEventListener('change',()=>{renderTracker();if(id==='metric')renderComparison();});
el('search').addEventListener('input',renderTracker);el('history-mode').addEventListener('change',renderComparison);
el('data-source').textContent=`Prices: ${data.data_sources.prices}. Fundamentals: ${data.data_sources.fundamentals}. Market session ${data.as_of}; generated ${data.created_at}. Method ${data.scoring_version}.`;
const mentions=data.image_mentions;
el('image-source').textContent=`${mentions.total_mentions??0} mentions; ${mentions.unique_tickers??0} unique tickers. Added repeated tickers: ${Object.entries(mentions.counts??{}).map(([t,n])=>`${t} (${n})`).join(', ')}. Frequency is a selection criterion only; it adds no score bonus.`;
renderSetups();renderIdeas();renderTracker();renderComparison();
})();
