#!/usr/bin/env python3
"""Send a changes-only digest AFTER publishing; never mail weekly/closed-day runs."""
import json
import os
import smtplib
import ssl
from datetime import datetime, timezone
from email.message import EmailMessage
from watchlist_runtime import DATA, market_gate
from watchlist import load

def main():
    x=load(DATA/'latest.json')
    # Dispatch/rebuild and weekend jobs are silent; notifications are for scheduled daily runs.
    if os.getenv('GITHUB_EVENT_NAME')!='schedule' or x['metadata'].get('refresh_kind')!='daily':return
    gate=market_gate(datetime.now(timezone.utc),'daily')
    if not gate['run'] or not gate['notify'] or not x['metadata'].get('notify'):return
    to=os.getenv('STOCK_EMAIL_TO');user=os.getenv('STOCK_EMAIL_USERNAME');pw=os.getenv('STOCK_EMAIL_APP_PASSWORD')
    if not all([to,user,pw]):
        print('Digest not sent: existing mail secrets are not configured. Dashboard remains the notification surface.');return
    msg=EmailMessage();msg['Subject']='Multi Bagger Action10 — '+x['run_date'];msg['From']=user;msg['To']=to
    changes=x['metadata'].get('material_changes',[])
    weekly=x['metadata'].get('weekly_review',{})
    msg.set_content('Action10 daily research monitor completed. No orders or automatic swaps.\n\n'+
        '\n'.join(changes[:20])+'\n\nWeekly review: '+str(weekly.get('status','not run'))+
        '\nPrices are previous completed regular-session closes. Research/source dates and unresolved gaps are on the dashboard.\n'+
        'https://skydiver1118.github.io/Automation/multi-bagger/')
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=ssl.create_default_context(),timeout=30) as smtp:
        smtp.login(user,pw);smtp.send_message(msg)
    print('Changes-only Multi Bagger digest sent.')

if __name__=='__main__':main()
