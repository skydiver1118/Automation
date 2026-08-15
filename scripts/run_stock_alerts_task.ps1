$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectRoot
. (Join-Path $ProjectRoot "scripts\stock_alert_common.ps1")

$EnvNames = @(
    "ALERT_SMTP_HOST",
    "ALERT_SMTP_PORT",
    "ALERT_SMTP_USER",
    "ALERT_SMTP_PASSWORD",
    "ALERT_EMAIL_FROM",
    "ALERT_EMAIL_TO"
)

foreach ($Name in $EnvNames) {
    $Value = [Environment]::GetEnvironmentVariable($Name, "User")
    if (-not [string]::IsNullOrWhiteSpace($Value)) {
        Set-Item -Path "Env:$Name" -Value $Value
    }
}

$Python = Get-StockAlertPython
& $Python scripts/run_stock_alerts.py --config configs/stock_alerts.local.json
