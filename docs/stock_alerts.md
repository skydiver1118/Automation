# Stock Alert Framework

This framework checks simple stock conditions, such as a close below SMA 50, and sends alerts by email. A phone text can be handled the same way if your mobile carrier still supports email-to-SMS addresses.

## Free Stack

- Data: `yfinance`, already included in this project, is good for free daily end-of-day checks.
- Email: Gmail SMTP works with `smtp.gmail.com`, port `587`, STARTTLS, and a Google App Password.
- Phone text: add your carrier's email-to-SMS address as a recipient, such as `number@carrier-gateway`. Carrier support changes, so test this before relying on it.
- Direct SMS without Gmail: Twilio is the practical test path. It has a free trial, then usage-based pricing.
- More reliable free push alerts: use a Discord webhook or Telegram bot webhook instead of SMS carrier gateways.
- Scheduler: Windows Task Scheduler on this machine is free and works well for a daily after-market run.

## Configure

Copy the example config and turn on the notification channel you want:

```powershell
Copy-Item configs/stock_alerts.example.json configs/stock_alerts.local.json
```

For Gmail SMTP, set secrets in your shell or in your user environment:

```powershell
$env:ALERT_SMTP_USER = "your.email@gmail.com"
$env:ALERT_SMTP_PASSWORD = "your-16-character-app-password"
$env:ALERT_EMAIL_FROM = "your.email@gmail.com"
$env:ALERT_EMAIL_TO = "your.email@gmail.com"
```

The expected variables are also listed in `.env.stock_alerts.example`. Do not put real passwords in committed files.

## Direct Cell Text With Twilio

Use this if you want a real SMS sent to your phone without Gmail.

1. Create a Twilio trial account.
2. Verify your cellphone number in Twilio. Trial accounts can usually send only to verified recipient numbers.
3. Get a Twilio phone number that supports SMS.
4. Copy your Account SID and Auth Token from the Twilio Console.
5. Set these variables:

```powershell
$env:TWILIO_ACCOUNT_SID = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
$env:TWILIO_AUTH_TOKEN = "your-twilio-auth-token"
$env:TWILIO_FROM_NUMBER = "+1yourTwilioNumber"
$env:TWILIO_TO_NUMBER = "+1yourCellNumber"
```

6. In `configs/stock_alerts.local.json`, set:

```json
"twilio_sms": {
  "enabled": true,
  "from": "+1yourTwilioNumber",
  "to": "+1yourCellNumber"
}
```

The environment variables override the config values, which is safer for phone numbers and credentials.

Then edit `configs/stock_alerts.local.json`:

- Set `notifications.email.enabled` to `true`.
- Put email recipients in `notifications.email.to`.
- For phone text, add the carrier gateway address as another recipient.
- Add more alert rules under `alerts`.

Send a direct Gmail SMTP test without checking stock data:

```powershell
python scripts/run_stock_alerts.py --config configs/stock_alerts.local.json --test-email
```

If plain `python` points to a minimal Python without dependencies, use the project Python directly:

```powershell
& "C:\Users\skydiver1118\AppData\Local\Programs\Python\Python314\python.exe" scripts/run_stock_alerts.py --config configs/stock_alerts.local.json --test-email
```

Or use the setup helper, which prompts for your Gmail address, recipient, and app password without putting them in a file:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup_gmail_alerts.ps1 -SendTest
```

For scheduled daily alerts, save the Gmail settings to your Windows user environment:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup_gmail_alerts.ps1 -SendTest -PersistUserEnv
```

This stores the Gmail App Password in your Windows user environment. It is convenient for Task Scheduler, but anyone with access to your Windows user account may be able to read it.

You can also double-click `setup_gmail_alerts.bat` from the project folder. It runs the same setup-and-test flow and keeps the window open so you can read the result.

Check the setup status:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_stock_alert_setup.ps1
```

Or double-click `check_stock_alert_setup.bat`.

After credentials are set, this can also send the Gmail SMTP test:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_stock_alert_setup.ps1 -TestEmail
```

Or double-click `send_gmail_test.bat`.

Supported conditions:

- `below_sma`
- `above_sma`
- `cross_below_sma`
- `cross_above_sma`

`notify_on` options:

- `enter`: alert once when the condition first becomes true.
- `always`: alert on every run while the condition is true.
- `change`: alert when the condition changes true or false.

## Run

Dry run first:

```powershell
python scripts/run_stock_alerts.py --config configs/stock_alerts.local.json --dry-run
```

Send real notifications:

```powershell
python scripts/run_stock_alerts.py --config configs/stock_alerts.local.json
```

The state file is written to `data/stock_alerts_state.json` so the same alert does not repeat every run unless you pass `--repeat` or set `notify_on` to `always`.

## Windows Task Scheduler

Create a daily task after the market close, for example 4:15 PM Eastern:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/register_stock_alert_task.ps1 -At 16:15
```

Keep secrets in your Windows user environment so Task Scheduler can read them.

The scheduled task runs `scripts/run_stock_alerts_task.ps1`, which reloads saved Windows user environment variables before sending alerts.

## Owned Stocks SMA50 Automation

Owned-stock symbols live in `configs/owned_stocks_sma50.json` under `symbols`.

Run a manual dry scan:

```powershell
& "C:\Users\skydiver1118\AppData\Local\Programs\Python\Python314\python.exe" -m src.strategy_lab.owned_stocks_sma50_alert --config configs/owned_stocks_sma50.json --dry-run
```

Run the real Gmail report:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_owned_stocks_sma50_task.ps1
```

Register or update the weekday 5:30 PM task:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/register_owned_stocks_sma50_task.ps1 -At 17:30
```

The report compares the current below-SMA50 list with `data/owned_stocks_sma50_state.json`. New below-SMA50 names are highlighted blue. Names removed from the prior below-SMA50 list are red and struck through.
