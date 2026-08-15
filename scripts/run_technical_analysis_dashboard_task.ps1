$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

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

$PythonCandidates = @(
    "C:\Users\skydiver1118\AppData\Local\Programs\Python\Python314\python.exe",
    "C:\Users\skydiver1118\AppData\Local\Python\bin\python.exe",
    (Get-Command python.exe -ErrorAction SilentlyContinue).Source
) | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique

$Python = $PythonCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $Python) {
    throw "No usable Python interpreter found."
}

$LogDir = Join-Path $ProjectRoot "reports\logs"
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogPath = Join-Path $LogDir "technical_analysis_dashboard_$Stamp.log"

try {
    "Starting technical-analysis dashboard refresh at $(Get-Date -Format o)" | Tee-Object -FilePath $LogPath
    "Python: $Python" | Tee-Object -FilePath $LogPath -Append
    & $Python "scripts\publish_technical_analysis_dashboard.py" @args *>&1 | Tee-Object -FilePath $LogPath -Append
    $ExitCode = $LASTEXITCODE
    "Finished technical-analysis dashboard refresh at $(Get-Date -Format o) with exit code $ExitCode" | Tee-Object -FilePath $LogPath -Append
    exit $ExitCode
} catch {
    $_ | Out-String | Tee-Object -FilePath $LogPath -Append | Out-Null
    throw
}
