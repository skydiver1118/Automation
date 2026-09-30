"""Real browser and HTTP verification for the separately published v2.2 layer."""
from __future__ import annotations
import argparse
import functools
import hashlib
import http.server
import json
import threading
from pathlib import Path
from urllib.request import Request, urlopen
from playwright.sync_api import sync_playwright

def run(base, output):
    base=base.rstrip('/')+'/';output=Path(output);output.mkdir(parents=True,exist_ok=True)
    def read(path):
        with urlopen(Request(base+path,headers={'Cache-Control':'no-cache'}),timeout=30) as r:return r.read()
    raw=read('v22/latest.json');data=json.loads(raw);build=json.loads(read('build.json'))
    assert data['source_snapshot_sha256']==build['monitoring_sha256']
    assert hashlib.sha256(raw).hexdigest()==build['v22']['artifact_sha256']
    assert data['counts']['members']==build['members']
    assert data['mode']=='shadow_only' and data['production_rank_effect'] is False
    assert all(s['v22_rank'] is None and s['v22_final_score'] is None and s['probability_5x'] is None for s in data['stocks'])
    assert all(s['shadow_feasibility_score'] is None for s in data['stocks'] if s['critical_reasons'])
    original=json.loads(read('monitoring/latest.json'))
    for before,after in zip(original['stocks'],data['stocks']):
        assert before['ticker']==after['ticker'] and before['metadata']['tier']==after['tier']
        assert before['metadata'].get('research',{}).get('price_date')==after['price_date']
    failures=[];opened=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1440,'height':1000})
        page.on('pageerror',lambda e:failures.append(str(e)))
        page.goto(base,wait_until='networkidle')
        page.wait_for_selector('#ranking tr')
        assert page.locator('#error').is_hidden()
        # The user's main dashboard now displays scenarios, not a second empty shell.
        page.locator('#group').select_option('all')
        for row in data['stocks']:
            text=page.locator('#ranking [data-t="'+row['ticker']+'"]').locator('xpath=ancestor::tr').inner_text()
            if row['scenarios']:
                expected=' / '.join(f"{row['scenarios'][n]['supportable_5y_multiple']:.2f}×" for n in ('bear','base','bull'))
                assert expected in text,(row['ticker'],'Missing main-page scenarios')
            else:assert 'Missing critical scenario data' in text
        page.locator('#ranking [data-t="IREN"]').click()
        assert 'v2.2 company analysis' in page.locator('#dialogBody').inner_text()
        page.locator('#close').click()
        page.locator('#history').select_option('2026-09-03')
        page.wait_for_function("document.querySelector('#auditBanner').textContent.includes('Historical snapshot')")
        assert 'No matching v2.2 record for this snapshot' in page.locator('#ranking').inner_text()
        page.locator('#tabV22').click()
        page.wait_for_function("document.querySelectorAll('#rows tr').length==="+str(build['members']))
        assert page.locator('#error').is_hidden()
        for stock in data['stocks']:
            ticker=stock['ticker'];page.locator('#rows [data-t="'+ticker+'"]').click()
            page.wait_for_selector('#reverseOutput')
            if stock['status']=='missing_critical_data':assert 'Missing Critical Data' in page.locator('#body').inner_text()
            if stock.get('company_review'):
                assert stock['company_review']['facts'] in page.locator('#body').inner_text()
                assert stock['company_review']['risk'] in page.locator('#body').inner_text()
            if stock['scenarios']:
                assert page.locator('#body .scenario-table tbody tr').count()==3
                assert page.locator('#body .scenario-case').count()==3
                if stock['scenario_assumptions']['model']=='enterprise_ebitda':
                    assert page.locator('#body .funding-table').count()==3
                    page.locator('#body .scenario-case').nth(1).locator('summary').click()
                    assert 'funding bridge' in page.locator('#body').inner_text().lower()
                if ticker=='IREN':page.screenshot(path=str(output/'v22_iren_funding_desktop.png'))
            if stock['reference_market_cap']:
                before=page.locator('#reverseOutput').inner_text();page.locator('#dilution').select_option('0.2')
                assert page.locator('#reverseOutput').inner_text()!=before
            else:assert 'unavailable' in page.locator('#reverseOutput').inner_text()
            opened.append(ticker);page.locator('#close').click()
        page.locator('#tier').select_option('action');assert page.locator('#rows tr').count()==build['action_count']
        page.locator('#tier').select_option('candidate');assert page.locator('#rows tr').count()==build['candidate_count']
        page.locator('#search').fill('ZZZ_ABSENT');assert 'No matching members' in page.locator('#rows').inner_text()
        page.locator('#search').fill('');page.locator('#tier').select_option('all')
        page.locator('#history').select_option(data['run_id']);page.wait_for_function("document.querySelector('#freshness').textContent.includes('Historical v2.2')")
        page.screenshot(path=str(output/'v22_desktop.png'),full_page=True)
        page.close()
        mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
        page=mobile.new_page();page.on('pageerror',lambda e:failures.append(str(e)))
        page.goto(base+'v22/',wait_until='networkidle');page.wait_for_function("document.querySelectorAll('#cards article').length==="+str(build['members']))
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        page.screenshot(path=str(output/'v22_mobile.png'),full_page=False)
        page.locator('#search').fill('IREN');page.locator('#cards [data-t="IREN"]').click()
        assert 'not a forecast or score' in page.locator('#body').inner_text().lower()
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        page.screenshot(path=str(output/'v22_iren_mobile.png'),full_page=False)
        page.locator('#close').click()
        page.route('**/v22/latest.json*',lambda route:route.fulfill(status=503,body='unavailable'))
        page.locator('#refresh').click();page.wait_for_function("!document.querySelector('#error').hidden")
        assert 'not a new refresh' in page.locator('#error').inner_text()
        assert page.locator('#cards article').count()==1
        mobile.close();browser.close()
    assert not failures,failures
    receipt={'status':'passed','base_url':base,'v22_version':build['v22']['version'],
        'source_market_session':data['source_market_session_date'], 'source_snapshot_sha256':data['source_snapshot_sha256'],
        'artifact_sha256':build['v22']['artifact_sha256'],'counts':data['counts'],'integrated_main_page_scenarios_verified':True,'historical_source_linkage_verified':True,'scenario_and_funding_details_verified':True,
        'details_opened':opened,'desktop_mobile_passed':True,'missing_data_and_failure_tests_passed':True,
        'javascript_errors':failures,'production_rank_effect':False}
    (output/'v22_verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
    return receipt

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--url');ap.add_argument('--site',type=Path);ap.add_argument('--output',type=Path,default=Path('v22-proof'));args=ap.parse_args()
    if bool(args.url)==bool(args.site):ap.error('Provide either --url or --site')
    if args.site:
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(args.site.resolve())))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        try:run('http://127.0.0.1:'+str(server.server_port)+'/',args.output)
        finally:server.shutdown()
    else:run(args.url,args.output)
