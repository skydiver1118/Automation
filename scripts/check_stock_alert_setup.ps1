param(
    [string]$TaskName = "Stock SMA Alerts",
    [switch]$TestEmail
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectRoot
. (Join-Path $ProjectRoot "scripts\stock_alert_common.ps1")
$Python = Get-StockAlertPython

function Get-MaskedValue {
    param(
        [string]$Name,
        [string]$Target = "Process"
    )

    $Value = [Environment]::GetEnvironmentVariable($Name, $Target)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        return "<not set>"
    }
    if ($Name -like "*PASSWORD*" -or $Name -like "*TOKEN*") {
        return "<set>"
    }
    return $Value
}

function Write-Check {
    param(
        [string]$Name,
        [bool]$Pass,
        [string]$Detail
    )

    $Status = if ($Pass) { "PASS" } else { "MISSING" }
    Write-Host "$Status - $Name - $Detail"
}

$ConfigPath = Join-Path $ProjectRoot "configs\stock_alerts.local.json"
$RunnerPath = Join-Path $ProjectRoot "scripts\run_stock_alerts.py"

Write-Host "Stock alert setup check"
Write-Host "Project: $ProjectRoot"
Write-Host ""

Write-Check "local config" (Test-Path $ConfigPath) $ConfigPath
Write-Check "runner" (Test-Path $RunnerPath) $RunnerPath

$RequiredEnv = @(
    "ALERT_SMTP_USER",
    "ALERT_SMTP_PASSWORD",
    "ALERT_EMAIL_FROM",
    "ALERT_EMAIL_TO"
)

Write-Host ""
Write-Host "Current PowerShell session:"
foreach ($Name in $RequiredEnv) {
    $Value = Get-MaskedValue -Name $Name -Target "Process"
    Write-Check $Name ($Value -ne "<not set>") $Value
}

Write-Host ""
Write-Host "Saved Windows user environment:"
foreach ($Name in $RequiredEnv) {
    $Value = Get-MaskedValue -Name $Name -Target "User"
    Write-Check $Name ($Value -ne "<not set>") $Value
}

Write-Host ""
$Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($Task) {
    Write-Check "scheduled task" $true "$TaskName is $($Task.State)"
} else {
    Write-Check "scheduled task" $false "$TaskName is not registered"
}

Write-Host ""
Write-Host "Dry-run stock alert check:"
& $Python scripts/run_stock_alerts.py --config configs/stock_alerts.local.json --dry-run --state "$env:TEMP\stock_alerts_setup_check_state.json"

if ($TestEmail) {
    foreach ($Name in $RequiredEnv) {
        $Value = [Environment]::GetEnvironmentVariable($Name, "User")
        if (-not [string]::IsNullOrWhiteSpace($Value)) {
            Set-Item -Path "Env:$Name" -Value $Value
        }
    }

    Write-Host ""
    Write-Host "Sending Gmail SMTP test:"
    & $Python scripts/run_stock_alerts.py --config configs/stock_alerts.local.json --test-email
}
