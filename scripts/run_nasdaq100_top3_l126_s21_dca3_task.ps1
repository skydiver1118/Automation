$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

. (Join-Path $ProjectRoot "scripts\stock_alert_common.ps1")

$LocalPython = "C:\Users\skydiver1118\AppData\Local\Python\bin\python.exe"
$RequiredPaths = @(
    (Join-Path $ProjectRoot ".localdeps"),
    (Join-Path $ProjectRoot ".deps"),
    (Join-Path $ProjectRoot ".deps2")
)

$CandidatePaths = @(
    "C:\Users\skydiver1118\AppData\Local\Python\bin\python.exe",
    "C:\Users\skydiver1118\AppData\Local\Programs\Python\Python314\python.exe"
)

$LogDir = Join-Path $ProjectRoot "reports\logs"
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogPath = Join-Path $LogDir "nasdaq100_top3_l126_s21_dca3_$Stamp.log"

try {
    if (Test-Path $LocalPython) {
        & $LocalPython "scripts\nasdaq100_top3_l126_s21_dca3_preflight.py" @args *>&1 | Tee-Object -FilePath $LogPath
        if ($LASTEXITCODE -eq 0) {
            exit 0
        }
        if ($LASTEXITCODE -ne 10) {
            throw "NASDAQ preflight failed with exit code $LASTEXITCODE. See $LogPath"
        }
    }

    try {
        $Python = Get-StockAlertPython -RequiredModules @("pandas", "numpy", "alpaca") -RequiredPaths $RequiredPaths -CandidatePaths $CandidatePaths
        & $Python "scripts\nasdaq100_top3_l126_s21_dca3_signal.py" @args *>&1 | Tee-Object -FilePath $LogPath
        if ($LASTEXITCODE -ne 0) {
            throw "NASDAQ executor exited with code $LASTEXITCODE"
        }
        exit 0
    } catch {
        $FailureText = (($_ | Out-String) -replace "\s+", " ").Trim()
        if ($FailureText.Length -gt 500) {
            $FailureText = $FailureText.Substring(0, 500)
        }
        if (-not (Test-Path $LocalPython)) {
            throw
        }
        & $LocalPython "scripts\nasdaq100_top3_l126_s21_dca3_fallback.py" --failure-reason $FailureText @args *>&1 | Tee-Object -FilePath $LogPath -Append
        exit $LASTEXITCODE
    }
} catch {
    $_ | Out-String | Tee-Object -FilePath $LogPath -Append | Out-Null
    throw
}
