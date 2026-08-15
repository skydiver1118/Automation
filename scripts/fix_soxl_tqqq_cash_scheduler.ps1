$ErrorActionPreference = "Stop"

$TaskName = "SOXL_TQQQ_Rotation_Cash_Daily_Scanner"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PowerShellExe = Join-Path $env:WINDIR "System32\WindowsPowerShell\v1.0\powershell.exe"
$Args = '-ExecutionPolicy Bypass -File scripts/run_soxl_tqqq_cash_daily_scanner_task.ps1 --agent "SOXL/TQQQ Rotation with cash" --env-file .env.alpaca --alpaca --execute --extended-hours --limit-offset-pct 0 --target-notional 10000 --qty 1 --email-to skydiver1118@gmail.com'

$Action = New-ScheduledTaskAction -Execute $PowerShellExe -Argument $Args -WorkingDirectory $ProjectRoot
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 4:10PM
$Settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 30) -StartWhenAvailable -MultipleInstances IgnoreNew
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType S4U -RunLevel Highest

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Force | Out-Null
Write-Host "Scheduled task updated: $TaskName"
Write-Host "Action: $PowerShellExe $Args"
Write-Host "WorkingDirectory: $ProjectRoot"
