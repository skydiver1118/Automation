'use strict';
const $=id=>document.getElementById(id);
let current=null, build=null, selected=null, loading=0;
const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const finite=x=>typeof x==='number'&&Number.isFinite(x);
const number=x=>finite(x)?x.toFixed(1):'—';
const money=x=>!finite(x)?'—':Math.abs(x)>=1e12?'$'+(x/1e12).toFixed(2)+'T':Math.abs(x)>=1e9?'$'+(x/1e9).toFixed(2)+'B':Math.abs(x)>=1e6?'$'+(x/1e6).toFixed(1)+'M':'$'+x.toFixed(2);
const pct=x=>finite(x)?(100*x).toFixed(1)+'%':'—';
const when=x=>{if(!x)return'Not recorded';const d=new Date(x);return Number.isNaN(d.valueOf())?'Invalid date':new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',dateStyle:'medium',timeStyle:'short'}).format(d)+' ET';};
const sourceLink=(u,label)=>{try{const v=new URL(u);return v.protocol==='https:'?'<a href="'+esc(v.href)+'" target="_blank" rel="noopener noreferrer">'+esc(label)+'</a>':esc(label);}catch{return esc(label);}};
async function get(path){const r=await fetch(path+(path.includes('?')?'&':'?')+'refresh='+Date.now(),{cache:'no-store'});if(!r.ok)throw Error(path+' HTTP '+r.status);return r.json();}
function hold(r){return r.status==='shadow_uncalibrated'?'Reviewed inputs · uncalibrated':'Missing Critical Data — unscored';}
function render(){
 const d=current;$('count').textContent=d.counts.members;$('hurdles').textContent=d.counts.capitalization_hurdles+' / '+d.counts.members;$('ready').textContent=d.counts.reviewed_scenario_sets;$('gaps').textContent=d.counts.missing_critical_scenario_data;
 const marketDates=[...new Set(d.stocks.map(r=>r.price_date).filter(Boolean))].sort();
 const dates=marketDates.length?marketDates.join(' / '):'Not available';
 const oldDates=marketDates.filter(x=>(Date.now()-new Date(x+'T20:00:00Z').valueOf())/86400000>4);
 $('freshness').textContent=($('history').value==='latest'?'Latest published':'Historical v2.2')+' · Source run: '+when(d.source_recorded_at)+' · Quote dates: '+dates+' · Page built: '+when(build?.built_at)+(oldDates.length?' · WARNING: some quotes are more than four calendar days old. Reloading this page does not fetch market prices.':'')+' · Scenario evaluation: '+d.evaluation_date_utc+' UTC';
 const attempt=build?.v22?.last_refresh_attempt;
 if($('history').value==='latest'&&attempt?.status==='failed_preserved_last_good')$('freshness').textContent+=' · MARKET REFRESH FAILED '+when(attempt.at)+': '+(attempt.error||'Source data unavailable')+'. Last good measurements retained.';
 const query=$('search').value.trim().toUpperCase();const tier=$('tier').value;
 const rows=d.stocks.filter(r=>(tier==='all'||r.tier===tier)&&(!query||r.ticker.includes(query)));
 $('rows').innerHTML=rows.map(r=>'<tr><td><button class="ticker" data-t="'+esc(r.ticker)+'">'+esc(r.ticker)+'</button></td><td>'+money(r.price)+'<small>'+esc(r.price_date||'No date')+'</small></td><td>'+esc(r.tier)+'</td><td>'+money(r.reference_market_cap)+'</td><td>'+number(r.mb_quality_score_v1)+'</td><td>'+money(r.required_5x_market_cap_no_dilution)+'</td><td>'+(finite(r.supportable_5y_multiple_base)?number(r.supportable_5y_multiple_base)+'×':'—')+'</td><td>'+number(r.shadow_feasibility_score)+'</td><td class="hold">'+hold(r)+'</td></tr>').join('')||'<tr><td class="empty" colspan="9">No matching members</td></tr>';
 $('cards').innerHTML=rows.map(r=>'<article class="card"><div class="card-head"><button class="ticker" data-t="'+esc(r.ticker)+'">'+esc(r.ticker)+'</button><strong>'+money(r.price)+'</strong></div><small>'+esc(r.tier)+' · Quote: '+esc(r.price_date||'not available')+'</small><p>Reference cap <strong>'+money(r.reference_market_cap)+'</strong> → 5× hurdle (no dilution) <strong>'+money(r.required_5x_market_cap_no_dilution)+'</strong></p><p>MB quality v1: '+number(r.mb_quality_score_v1)+' · v2.2 feasibility: '+number(r.shadow_feasibility_score)+'</p><p class="hold">'+hold(r)+'</p></article>').join('')||'<p class="empty">No matching members</p>';
 document.querySelectorAll('[data-t]').forEach(e=>e.addEventListener('click',()=>openDetail(e.dataset.t)));
 $('checks').innerHTML=Object.entries(d.calibration.checks).map(([k,v])=>'<p><span class="pending">'+(v?'Evidence supplied':'Not passed')+'</span>'+esc(k.replaceAll('_',' '))+'</p>').join('')+'<p>'+sourceLink(d.calibration.last_known_collection_attempt,'Last known cohort-collection attempt')+' — '+esc(d.calibration.last_known_collection_result)+'. No completed OOS calibration is claimed.</p>';
 $('limitations').innerHTML='<ul>'+d.limitations.map(s=>'<li>'+esc(s)+'</li>').join('')+'</ul>';
 const requested=new URLSearchParams(location.search).get('ticker');if(requested&&d.stocks.some(r=>r.ticker===requested)&&!selected)openDetail(requested);
}
function field(k,v){return'<tr><th>'+esc(k)+'</th><td>'+esc(v)+'</td></tr>';}
function openDetail(ticker){
 selected=current.stocks.find(r=>r.ticker===ticker);const r=selected;$('title').textContent=ticker+' · v2.2 evidence';
 let html='<p class="notice"><strong>'+hold(r)+'.</strong> Final v2.2 score and P(5×): unavailable. This panel does not promote the stock or create an entry signal.</p>';
 html+='<table>'+field('Quote / market date',money(r.price)+' / '+(r.price_date||'unavailable'))+field('Reference market cap',money(r.reference_market_cap))+field('Market-cap basis',r.market_cap_basis)+field('Required equity for 5×, unchanged shares',money(r.required_5x_market_cap_no_dilution))+field('Additional equity required, unchanged shares',money(r.incremental_equity_required_no_dilution))+field('Trailing revenue / period end',money(r.revenue_ttm)+' / '+(r.financial_period_end||'unavailable'))+field('Fundamental review',when(r.financial_reviewed_at))+field('Base scenario: dilution-adjusted 5× hurdle',money(r.required_5x_market_cap_dilution_adjusted))+field('Base supportable future COMPANY equity',money(r.supportable_terminal_equity_value_base))+field('Base per-share return multiple',finite(r.supportable_5y_multiple_base)?number(r.supportable_5y_multiple_base)+'×':'Unscored')+field('Base feasibility gap (1 = reaches 5×)',number(r.feasibility_gap_base))+'</table>';
 html+='<h3>What is missing?</h3><ul>'+r.critical_reasons.map(s=>'<li>'+esc(s)+'</li>').join('')+'</ul>';
 if(r.scenarios){html+='<h3>Reviewed scenario assumptions—not promises</h3>';for(const n of ['bear','base','bull']){const s=r.scenarios[n];const record=r.scenario_assumptions.scenarios[n];html+='<details class="panel"><summary>'+esc(n.toUpperCase())+' · '+number(s.supportable_5y_multiple)+'× per share</summary><div class="caption"><p>'+esc(record.label)+'</p><table>'+Object.entries(record.inputs).map(([k,v])=>field(k.replaceAll('_',' '),v)).join('')+'</table>'+Object.entries(record.assumption_evidence).map(([k,v])=>'<p><strong>'+esc(k)+'</strong>: '+esc(v.rationale)+'</p>').join('')+'</div></details>';}}
 html+='<h3>Reverse 5× hurdle: what would need to happen?</h3><section class="reverse"><p><strong>Hypothetical sensitivity—not a forecast or score.</strong> Select explicit assumptions. P/E applies to earnings after interest and tax, so debt is not subtracted twice. Restricted cash, project economics and financing still need independent review.</p><div class="reverse-controls"><label>Cumulative share dilution<select id="dilution"><option value="0">0% — unchanged shares</option><option value="0.2">20% — hypothetical</option><option value="0.5">50% — hypothetical</option></select></label><label>Normalized net margin<select id="margin"><option value="0.1">10% — hypothetical</option><option value="0.2" selected>20% — hypothetical</option><option value="0.3">30% — hypothetical</option></select></label><label>Terminal P/E<select id="pe"><option value="15">15× — hypothetical</option><option value="20" selected>20× — hypothetical</option><option value="30">30× — hypothetical</option></select></label></div><div id="reverseOutput" class="reverse-output" aria-live="polite"></div></section>';
 html+='<h3>Sources and warnings</h3><p>'+sourceLink(r.primary_source,'Saved primary financial source')+' · '+sourceLink(r.market_source,'Saved market source')+'</p>';
 if(r.scenario_assumptions?.sources){html+='<ul>'+Object.entries(r.scenario_assumptions.sources).map(([id,s])=>'<li>'+sourceLink(s.url,id)+' · '+esc(s.as_of)+'</li>').join('')+'</ul>';}
 html+='<ul>'+r.warnings.map(s=>'<li>'+esc(s)+'</li>').join('')+'</ul><details><summary>Financial dependency fingerprint</summary><p>'+esc(r.financial_basis_sha256)+'</p><p>A reviewed scenario must match this fingerprint. A data change invalidates old assumptions instead of silently reusing them.</p></details>';
 $('body').innerHTML=html;for(const id of ['dilution','margin','pe'])$(id).addEventListener('change',reverse);reverse();if(!$('detail').open)$('detail').showModal();
}
function reverse(){const v=selected.reverse_sensitivities.find(s=>s.dilution_5y===Number($('dilution').value)&&s.net_margin===Number($('margin').value)&&s.terminal_pe===Number($('pe').value));$('reverseOutput').innerHTML=v?'<p>Required future COMPANY equity: <strong>'+money(v.required_terminal_equity)+'</strong></p><p>Required annual earnings to common: <strong>'+money(v.required_common_net_income)+'</strong></p><p>Required annual revenue: <strong>'+money(v.required_revenue)+'</strong></p><p>Required five-year revenue CAGR: <strong>'+pct(v.required_revenue_cagr)+'</strong></p><small>Numbers are requirements under the selected assumptions, not estimates of future outcomes. No dividend contribution is assumed.</small>':'<p class="hold">Capitalization or comparable revenue is unavailable. Missing inputs are not replaced with zero.</p>';}
async function load(path='./latest.json'){
 const generation=++loading;$('refresh').disabled=true;
 try{let [data,b]=await Promise.all([get(path),get('../build.json')]);if(generation!==loading)return;
 if(data.methodology!=='MB_5X_FEASIBILITY_SHADOW_V2_2'||data.production_rank_effect!==false)throw Error('Invalid v2.2 methodology/rank policy');
 if(path==='./latest.json'&&data.source_snapshot_sha256!==b.monitoring_sha256)throw Error('Deployment still propagating: source snapshots differ. Reload in a moment; stale data are not a fresh run.');
 current=data;build=b;$('error').hidden=true;render();
 }catch(e){if(generation===loading){$('error').hidden=false;$('error').textContent='Published v2.2 data unavailable or inconsistent. '+e.message+(current?' Last loaded data remain visible and are not a new refresh.':'');}}
 finally{if(generation===loading)$('refresh').disabled=false;}
}
$('tier').addEventListener('change',()=>current&&render());$('search').addEventListener('input',()=>current&&render());$('close').addEventListener('click',()=>$('detail').close());$('detail').addEventListener('close',()=>{selected=null;});
$('refresh').addEventListener('click',()=>{$('history').value='latest';load();});
$('history').addEventListener('change',()=>{selected=null;load($('history').value==='latest'?'./latest.json':'./runs/'+encodeURIComponent($('history').value)+'.json');});
get('./history.json').then(h=>{for(const r of [...h.runs].reverse()){const option=document.createElement('option');option.value=r.run_id;option.textContent=r.evaluation_date_utc+' · '+(r.source_market_session_date||'no market date')+' · '+r.run_id.slice(0,6);$('history').append(option);}}).catch(()=>{});
load();
