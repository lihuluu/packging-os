#requires -version 5.1
param(
    [string]$Root,
    [switch]$Execute
)

$ErrorActionPreference = "Stop"

if (-not $Root) {
    $Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")).Path
}

$ProjectsDir = Join-Path $Root "Workspace\Projects"
if (-not (Test-Path $ProjectsDir)) {
    Write-Error "Cannot find Workspace\Projects under $Root"
    exit 1
}

function Test-ProjectTempItem {
    param([System.IO.FileSystemInfo]$Item)

    if ($Item.PSIsContainer) {
        return $Item.Name -eq "__pycache__"
    }

    $name = $Item.Name
    return (
        $name -eq ".DS_Store" -or
        $name -eq "Thumbs.db" -or
        $name -eq "desktop.ini" -or
        $name.StartsWith("~$") -or
        $name.EndsWith(".tmp") -or
        $name.Contains(".tmp.") -or
        $name.EndsWith(".bak") -or
        $name.EndsWith(".log") -or
        ($name -eq ".gitkeep" -and $Item.Length -eq 0)
    )
}

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "Packging OS - project temp cleanup"
Write-Host "Scan directory: $ProjectsDir"
Write-Host ("Mode: " + ($(if ($Execute) { "delete" } else { "dry-run" })))
Write-Host ""

$items = Get-ChildItem -Path $ProjectsDir -Recurse -Force | Where-Object { Test-ProjectTempItem $_ }
$deleted = 0
$errors = 0

foreach ($item in $items) {
    if ($Execute) {
        try {
            Remove-Item -LiteralPath $item.FullName -Force -Recurse
            Write-Host "  [deleted] $($item.FullName)"
            $deleted++
        } catch {
            Write-Error "  [failed] $($item.FullName): $($_.Exception.Message)"
            $errors++
        }
    } else {
        Write-Host "  [would delete] $($item.FullName)"
    }
}

Write-Host ""
if ($Execute) {
    Write-Host "Done: found $($items.Count), deleted $deleted, failed $errors."
    if ($errors -gt 0) { exit 1 }
    exit 0
}

if ($items.Count -eq 0) {
    Write-Host "No project temp files found."
} else {
    Write-Host "Found $($items.Count) project temp files. Re-run with -Execute to delete them."
}
exit 0
