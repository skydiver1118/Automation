$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$Python = "C:\Users\skydiver1118\AppData\Local\Python\bin\python.exe"
if (-not (Test-Path $Python)) {
    throw "Required interpreter not found: $Python"
}

$LogDir = Join-Path $ProjectRoot "reports\logs"
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogPath = Join-Path $LogDir "soxl_tqqq_cash_scanner_$Stamp.log"

try {
    & $Python "scripts\soxl_tqqq_cash_signal_scanner_stdlib.py" --allow-stale-fallback @args *>&1 | Tee-Object -FilePath $LogPath
    exit $LASTEXITCODE
} catch {
    $_ | Out-String | Tee-Object -FilePath $LogPath -Append | Out-Null
    throw
}
