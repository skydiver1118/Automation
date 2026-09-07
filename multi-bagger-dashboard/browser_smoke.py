"""Public/UI smoke tests. No trades, notifications, membership changes or data writes."""
from __future__ import annotations
import argparse,functools,http.server,json,threading,time
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright


def run(base: str, output: Path, public: bool=False) -> dict:
    output.mkdir(parents=True,exist_ok=True)
    base=base.rstrip('/')+'/'
    def read(path):
        with urlopen(base+path,timeout=30) as r:return json.load(r)
    build=read('build.json');data=read('monitoring/latest.json')
    assert build.get('evidence_audit',{}).get('scorecards_with_audit',0)>=30,'Evidence repair not published'
    assert len(data['stocks'])>=30 and data['metadata']['action_count']==10
    assert not build['automatic_swaps'] and build['candidate_first']
    assert not build['full_six_pass_complete'],'Input audit cannot masquerade as full research'
    counts={k:sum(s['metadata']['tier']==k for s in data['stocks']) for k in ['action','candidate']}
    checked=[];errors=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
        context=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
        page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(base,wait_until='networkidle');page.wait_for_function("document.querySelectorAll('#ranking tr').length===10")
        assert 'source-backed scorecards' in page.locator('#auditBanner').inner_text()
        assert 'not yet certified' in page.locator('#auditBanner').inner_text()
        assert page.locator('#error').is_hidden()
        page.locator('#group').select_option('all')
        assert page.locator('#ranking tr').count()==len(data['stocks'])
        for stock in data['stocks']:
            if not stock['metadata'].get('audit_file'):continue
            ticker=stock['ticker']
            page.locator('#ranking [data-t="'+ticker+'"]').click()
            page.wait_for_selector('#evidenceDetail .quarter-table',timeout=20000)
            assert 'Source-backed score audit' in page.locator('#evidenceDetail').inner_text()
            assert page.locator('#evidenceDetail .quarter-table thead th').count()==9
            assert page.locator('#evidenceDetail .audit-pass').count()==6
            if ticker=='POET':assert 'Missing' in page.locator('#evidenceDetail').inner_text()
            if ticker=='FIGR':assert 'Kiavi' in page.locator('#dialogBody').inner_text()
            checked.append(ticker);page.locator('#close').click()
        page.locator('#search').fill('ZZZ_NO_SUCH_ISSUER')
        assert 'No matching members' in page.locator('#ranking').inner_text()
        page.locator('#reset').click();assert page.locator('#ranking tr').count()==10
        page.locator('#tabWeekly').click();assert page.locator('#weeklyPanel').is_visible()
        page.locator('#tabCandidates').click();assert page.locator('#ranking tr').count()==counts['candidate']
        page.locator('#history').select_option('2026-09-03')
        page.wait_for_function("document.querySelectorAll('#ranking tr').length===20")
        assert 'Historical snapshot' in page.locator('#auditBanner').inner_text()
        page.screenshot(path=str(output/'desktop_history.png'))
        context.close()
        mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=1,reduced_motion='reduce')
        page=mobile.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(base,wait_until='networkidle');page.wait_for_function("document.querySelectorAll('#cards article').length===10")
        assert page.locator('#passCards article').count()==10
        assert page.locator('.pass-desktop').is_hidden()
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        page.screenshot(path=str(output/'mobile_action.png'))
        page.locator('#tabCandidates').click();assert page.locator('#cards article').count()==counts['candidate']
        page.locator('#cards [data-t="POET"]').click();page.wait_for_selector('#evidenceDetail .quarter-table')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        page.screenshot(path=str(output/'mobile_evidence.png'))
        mobile.close()
        # A failed evidence fetch must leave the score flagged and show an explicit error.
        failed=browser.new_context(viewport={'width':1440,'height':1000})
        failed.route('**/evidence_audit/**/ETN.json',lambda route:route.fulfill(status=503,body='Evidence temporarily unavailable'))
        page=failed.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(base,wait_until='networkidle');page.locator('#ranking [data-t="ETN"]').click()
        page.wait_for_function("document.querySelector('#evidenceDetail').textContent.includes('Evidence record unavailable')")
        assert 'Do not treat this score as fully supported' in page.locator('#evidenceDetail').inner_text()
        failed.close();browser.close()
    assert not errors,errors
    receipt={'status':'passed','test_scope':'Public HTTP + Chromium desktop/mobile with a separate injected evidence-unavailable test' if public else 'Local HTTP + real Chromium desktop/mobile; missing-evidence test injected at fetch boundary','base_url':base,'built_at':build.get('built_at'),'monitoring_sha256':build.get('monitoring_sha256'),'members':len(data['stocks']),'counts':counts,'audits_opened':len(checked),'tickers_checked':checked,'javascript_errors':errors,'full_research_certification_claimed':False}
    (output/'browser_verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2));return receipt

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--site',type=Path);ap.add_argument('--url');ap.add_argument('--output',type=Path,default=Path('browser-proof'));a=ap.parse_args()
    if bool(a.site)==bool(a.url):ap.error('Provide exactly one of --site or --url')
    if a.site:
        handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(a.site.resolve()))
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler);threading.Thread(target=server.serve_forever,daemon=True).start()
        try:run(f'http://127.0.0.1:{server.server_port}/',a.output)
        finally:server.shutdown()
    else:run(a.url,a.output,public=True)
