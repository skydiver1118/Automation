$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    throw "Scanner environment not installed. Run install_scanner.ps1 first."
}

Set-Location $Root
if ($args.Count -eq 0) {
    & $Python scripts\soxl_tqqq_cash_signal_scanner.py --agent "SOXL/TQQQ Rotation with cash"
} else {
    & $Python scripts\soxl_tqqq_cash_signal_scanner.py @args
}
exit $LASTEXITCODE
