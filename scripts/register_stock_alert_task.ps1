param(
    [string]$TaskName = "Stock SMA Alerts",
    [string]$At = "16:15",
    [switch]$RunOnceNow
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
. (Join-Path $ProjectRoot "scripts\stock_alert_common.ps1")
$PowerShell = (Get-Command powershell.exe).Source
$Argument = "-ExecutionPolicy Bypass -File `"scripts\run_stock_alerts_task.ps1`""

$Action = New-ScheduledTaskAction -Execute $PowerShell -Argument $Argument -WorkingDirectory $ProjectRoot
$Trigger = New-ScheduledTaskTrigger -Daily -At $At
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description "Run local stock SMA alert checks and send configured notifications." `
    -Force | Out-Null

Write-Host "Registered scheduled task '$TaskName' for daily run at $At."

if ($RunOnceNow) {
    Start-ScheduledTask -TaskName $TaskName
    Write-Host "Started scheduled task '$TaskName'."
}
