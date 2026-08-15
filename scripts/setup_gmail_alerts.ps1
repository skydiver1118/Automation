param(
    [switch]$SendTest,
    [switch]$PersistUserEnv
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectRoot
. (Join-Path $ProjectRoot "scripts\stock_alert_common.ps1")

$Gmail = Read-Host "Sender Gmail address"
$Recipient = Read-Host "Recipient email or phone gateway address"
$PasswordSecure = Read-Host "Gmail App Password" -AsSecureString
$PasswordPtr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($PasswordSecure)

try {
    $Password = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($PasswordPtr)

    $env:ALERT_SMTP_HOST = "smtp.gmail.com"
    $env:ALERT_SMTP_PORT = "587"
    $env:ALERT_SMTP_USER = $Gmail
    $env:ALERT_SMTP_PASSWORD = $Password
    $env:ALERT_EMAIL_FROM = $Gmail
    $env:ALERT_EMAIL_TO = $Recipient

    Write-Host "Gmail alert environment variables are set for this PowerShell session."

    if ($PersistUserEnv) {
        [Environment]::SetEnvironmentVariable("ALERT_SMTP_HOST", "smtp.gmail.com", "User")
        [Environment]::SetEnvironmentVariable("ALERT_SMTP_PORT", "587", "User")
        [Environment]::SetEnvironmentVariable("ALERT_SMTP_USER", $Gmail, "User")
        [Environment]::SetEnvironmentVariable("ALERT_SMTP_PASSWORD", $Password, "User")
        [Environment]::SetEnvironmentVariable("ALERT_EMAIL_FROM", $Gmail, "User")
        [Environment]::SetEnvironmentVariable("ALERT_EMAIL_TO", $Recipient, "User")
        Write-Host "Gmail alert environment variables were also saved to your Windows user environment."
        Write-Host "Open a new PowerShell window before relying on the saved variables."
    }

    if ($SendTest) {
        $Python = Get-StockAlertPython
        & $Python scripts/run_stock_alerts.py --config configs/stock_alerts.local.json --test-email
    } else {
        Write-Host "To send a test email now, run:"
        Write-Host "& `"$((Get-StockAlertPython))`" scripts/run_stock_alerts.py --config configs/stock_alerts.local.json --test-email"
    }
}
finally {
    if ($PasswordPtr -ne [IntPtr]::Zero) {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($PasswordPtr)
    }
}
