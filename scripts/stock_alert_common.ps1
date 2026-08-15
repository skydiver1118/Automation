function Get-StockAlertPython {
    param(
        [string[]]$RequiredModules = @(),
        [string[]]$RequiredPaths = @(),
        [string[]]$CandidatePaths = @()
    )

    $KnownLocalPython = "C:\Users\skydiver1118\AppData\Local\Python\bin\python.exe"
    $KnownPython = "C:\Users\skydiver1118\AppData\Local\Programs\Python\Python314\python.exe"
    $Candidates = @()
    if ($env:SOXL_SCANNER_PYTHON) {
        $Candidates += $env:SOXL_SCANNER_PYTHON
    }
    if ($CandidatePaths.Count -gt 0) {
        $Candidates += $CandidatePaths
    }
    if (Test-Path $KnownLocalPython) {
        $Candidates += $KnownLocalPython
    }
    if (Test-Path $KnownPython) {
        $Candidates += $KnownPython
    }

    try {
        $CommandPython = (Get-Command python -ErrorAction Stop).Source
        if ($CommandPython) {
            $Candidates += $CommandPython
        }
    } catch {
    }

    $Failures = @()
    foreach ($Candidate in ($Candidates | Select-Object -Unique)) {
        try {
            & $Candidate --version *> $null
            if ($LASTEXITCODE -ne 0) {
                $Failures += "$Candidate -> --version exit code $LASTEXITCODE"
                continue
            }

            if ($RequiredModules.Count -gt 0) {
                $InlinePathJson = ($RequiredPaths | ConvertTo-Json -Compress)
                $InlineModuleJson = ($RequiredModules | ConvertTo-Json -Compress)
                $InlineImportCode = ($RequiredModules | ForEach-Object {
                    "import $_"
                }) -join "`n"
                $InlineScript = @"
import json
import os
import site
import sys
paths = json.loads(r'''$InlinePathJson''')
modules = json.loads(r'''$InlineModuleJson''')
for candidate_path in paths:
    if not candidate_path:
        continue
    if not os.path.isdir(candidate_path):
        continue
    try:
        os.listdir(candidate_path)
    except Exception:
        continue
    site.addsitedir(candidate_path)
for module_name in modules:
    __import__(module_name)
$InlineImportCode
print("ok")
"@
                $InlineScript | & $Candidate - 2>&1 | Out-String | Tee-Object -Variable ProbeOutput *> $null
                if ($LASTEXITCODE -ne 0) {
                    $ProbeOutput = ($ProbeOutput | Out-String).Trim()
                    if (-not $ProbeOutput) {
                        $ProbeOutput = "missing required modules"
                    }
                    $Failures += "$Candidate -> $ProbeOutput"
                    continue
                }
            }

            if ($LASTEXITCODE -eq 0) {
                return $Candidate
            }
        } catch {
            $Failures += "$Candidate -> $($_.Exception.Message)"
        }
    }

    $FailureText = if ($Failures.Count -gt 0) { $Failures -join "; " } else { "no candidates discovered" }
    throw "Unable to find a runnable Python interpreter for stock alert tasks. Attempts: $FailureText"
}
