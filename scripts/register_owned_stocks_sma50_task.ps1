param(
    [string]$TaskName = "Owned Stocks SMA50 Alerts",
    [string]$At = "17:30"
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$PowerShell = (Get-Command powershell.exe).Source
$Argument = "-ExecutionPolicy Bypass -File `"scripts\run_owned_stocks_sma50_task.ps1`""

$Action = New-ScheduledTaskAction -Execute $PowerShell -Argument $Argument -WorkingDirectory $ProjectRoot
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At $At
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description "Scan owned stocks below SMA50 and email an HTML day-over-day diff." `
    -Force | Out-Null

Write-Host "Registered scheduled task '$TaskName' for weekdays at $At."
