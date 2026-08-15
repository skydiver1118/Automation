$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3.14 --version *> $null
    if ($LASTEXITCODE -eq 0) {
        & py -3.14 -m venv .venv
    } else {
        & py -3 -m venv .venv
    }
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python -m venv .venv
} else {
    throw "Python was not found. Install Python 3.14 and rerun this script."
}

$Python = Join-Path $Root ".venv\Scripts\python.exe"
& $Python -m pip install --upgrade pip
& $Python -m pip install -r requirements.txt
& $Python -m py_compile scripts\soxl_tqqq_cash_signal_scanner.py

if (-not (Test-Path .env.alpaca)) {
    Copy-Item .env.alpaca.example .env.alpaca
}

Write-Host "Scanner environment installed at $Root\.venv"
Write-Host "Next: edit $Root\.env.alpaca, then run .\run_scanner.ps1"
