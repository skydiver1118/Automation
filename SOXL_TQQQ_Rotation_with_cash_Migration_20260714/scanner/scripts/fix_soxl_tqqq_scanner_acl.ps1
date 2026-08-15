$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$AclTargets = @(
    "C:\Users\skydiver1118\AppData\Local\Programs\Python\Python314",
    "C:\Users\skydiver1118\AppData\Local\Python\pythoncore-3.14-64",
    (Join-Path $ProjectRoot ".deps"),
    (Join-Path $ProjectRoot ".deps2"),
    (Join-Path $ProjectRoot ".localdeps"),
    (Join-Path $ProjectRoot "vendor"),
    (Join-Path $ProjectRoot "vendor_py314")
)

$Principals = @(
    "$env:USERDOMAIN\$env:USERNAME",
    "Users"
)

foreach ($Target in $AclTargets) {
    if (-not (Test-Path $Target)) {
        Write-Host "skip_missing $Target"
        continue
    }
    foreach ($Principal in $Principals) {
        Write-Host "granting $Principal on $Target"
        $Output = & icacls $Target /grant "${Principal}:(OI)(CI)RX" /T /C 2>&1
        $OutputText = ($Output | Out-String)
        if ($OutputText -match "Access is denied") {
            throw "ACL grant failed for $Target ($Principal): Access is denied"
        }
    }
}

Write-Host "ACL remediation completed."
