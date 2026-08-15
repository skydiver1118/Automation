$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Runner = Join-Path $Root "run_scanner.ps1"
$TaskName = "SOXL_TQQQ_Rotation_Cash_Daily_Scanner"
$PowerShell = Join-Path $env:WINDIR "System32\WindowsPowerShell\v1.0\powershell.exe"
$Arguments = '-NoProfile -ExecutionPolicy Bypass -File "' + $Runner + '" --agent "SOXL/TQQQ Rotation with cash" --env-file .env.alpaca --alpaca --execute --extended-hours --limit-offset-pct 0 --qty 1'

if (-not (Test-Path (Join-Path $Root ".venv\Scripts\python.exe"))) {
    throw "Run install_scanner.ps1 before installing the task."
}
if (-not (Test-Path (Join-Path $Root ".env.alpaca"))) {
    throw "Create and validate .env.alpaca before installing the task."
}

$Action = New-ScheduledTaskAction -Execute $PowerShell -Argument $Arguments -WorkingDirectory $Root
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 4:10PM
$Settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 30) -StartWhenAvailable -MultipleInstances IgnoreNew
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType S4U -RunLevel Highest
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Force | Out-Null

Write-Host "Installed scheduled task: $TaskName"
Write-Host "Schedule: weekdays at 4:10 PM in the destination PC's local time zone"
