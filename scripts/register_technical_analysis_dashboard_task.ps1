param(
    [string]$TaskName = "Technical_Analysis_Dashboard_Scanner",
    [string]$At = "16:40",
    [string]$EmailTo = "skydiver1118@gmail.com",
    [switch]$RunOnceNow
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PowerShell = (Get-Command powershell.exe).Source
$Argument = "-ExecutionPolicy Bypass -File `"scripts\run_technical_analysis_dashboard_task.ps1`" --email-to $EmailTo"

$Action = New-ScheduledTaskAction -Execute $PowerShell -Argument $Argument -WorkingDirectory $ProjectRoot
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At $At
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 60)
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType S4U -RunLevel Highest
$Description = "Build and publish the technical-analysis dashboard from the TradingAgents watchlist after market close."

try {
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Principal $Principal `
        -Description $Description `
        -Force | Out-Null
} catch {
    Write-Warning "S4U/highest-principal registration failed: $($_.Exception.Message)"
    Write-Warning "Falling back to current-user registration."
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Description $Description `
        -Force | Out-Null
}

Write-Host "Registered scheduled task '$TaskName' for weekdays at $At."

if ($RunOnceNow) {
    Start-ScheduledTask -TaskName $TaskName
    Write-Host "Started scheduled task '$TaskName'."
}
