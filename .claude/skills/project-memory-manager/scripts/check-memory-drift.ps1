# check-memory-drift.ps1 - 项目卡漂移检查脚本 (PowerShell)
#
# 用法：
#   powershell -ExecutionPolicy Bypass -File check-memory-drift.ps1
#   powershell -ExecutionPolicy Bypass -File check-memory-drift.ps1 -All
#   powershell -ExecutionPolicy Bypass -File check-memory-drift.ps1 -Threshold 14
#
# 功能：
#   扫描 Workspace/Projects/ 下的所有项目，
#   检查每个项目的 project-memory-card.md 是否落后于该项目下的最新文件。
#   输出汇总表，并对落后超过阈值的项目发出警告。

[CmdletBinding()]
param(
    [string]$Root,
    [int]$Threshold = 7,
    [switch]$All
)

$ErrorActionPreference = "Stop"

# 推断仓库根目录
if (-not $Root) {
    $Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")).Path
}
$Root = (Resolve-Path $Root).Path

$ProjectsDir = Join-Path $Root "Workspace\Projects"
if (-not (Test-Path $ProjectsDir)) {
    Write-Error "Workspace\Projects not found under $Root"
    exit 1
}

$CardRelative = "00_Project_Control\project-memory-card.md"
$SkipDirs = @("00_Project_Control")
$SkipExtensions = @(".tmp", ".bak", ".log")
$SkipNames = @(".DS_Store", "Thumbs.db", "desktop.ini", ".gitkeep")

$DriftProjects = [System.Collections.Generic.List[PSObject]]::new()
$OkProjects = [System.Collections.Generic.List[PSObject]]::new()
$NoCardProjects = [System.Collections.Generic.List[string]]::new()
$NoOtherFilesProjects = [System.Collections.Generic.List[string]]::new()

$projectDirs = Get-ChildItem -Path $ProjectsDir -Directory | Where-Object { -not $_.Name.StartsWith(".") }

foreach ($proj in $projectDirs) {
    $cardPath = Join-Path $proj.FullName $CardRelative
    if (-not (Test-Path $cardPath)) {
        $NoCardProjects.Add($proj.Name)
        continue
    }

    $cardTime = (Get-Item $cardPath).LastWriteTimeUtc

    # 查找排除 00_Project_Control 后的最新文件
    $latestFile = $null
    $latestTime = [datetime]::MinValue

    Get-ChildItem -Path $proj.FullName -Recurse -File | Where-Object {
        $relative = $_.FullName.Substring($proj.FullName.Length + 1)
        $topDir = $relative.Split("\")[0]
        ($topDir -notin $SkipDirs) -and
        ($_.Extension -notin $SkipExtensions) -and
        ($_.Name -notin $SkipNames)
    } | ForEach-Object {
        if ($_.LastWriteTimeUtc -gt $latestTime) {
            $latestTime = $_.LastWriteTimeUtc
            $latestFile = $_
        }
    }

    if ($null -eq $latestFile) {
        $NoOtherFilesProjects.Add($proj.Name)
        continue
    }

    $delta = ($latestTime - $cardTime).Days

    if ($delta -ge $Threshold) {
        $latestRel = $latestFile.FullName.Substring($proj.FullName.Length + 1)
        $DriftProjects.Add([PSCustomObject]@{
            Name       = $proj.Name
            CardTime   = $cardTime
            LatestTime = $latestTime
            Days       = $delta
            LatestFile = $latestRel
        })
    }
    else {
        $OkProjects.Add([PSCustomObject]@{
            Name       = $proj.Name
            CardTime   = $cardTime
            LatestTime = $latestTime
        })
    }
}

# Output
$now = Get-Date -Format "yyyy-MM-dd HH:mm"
Write-Output "Packging OS - project card drift check"
Write-Output "Scan dir: $ProjectsDir"
Write-Output "Threshold: $Threshold days"
Write-Output "Scan time: $now"
Write-Output ""

if ($DriftProjects.Count -gt 0) {
    Write-Output "DRIFT ($($DriftProjects.Count) projects need card update)"
    Write-Output ""
    foreach ($p in $DriftProjects) {
        $c = Get-Date $p.CardTime -Format "yyyy-MM-dd"
        $l = Get-Date $p.LatestTime -Format "yyyy-MM-dd"
        Write-Output "  $($p.Name) | card=$c latest=$l drift=$($p.Days)d | $($p.LatestFile)"
    }
    Write-Output ""
}
else {
    Write-Output "OK - no drift detected (all cards within threshold)."
    Write-Output ""
}

if ($All -and $OkProjects.Count -gt 0) {
    Write-Output "OK - cards up to date ($($OkProjects.Count) projects)"
    foreach ($p in $OkProjects) {
        $c = Get-Date $p.CardTime -Format "yyyy-MM-dd"
        $l = Get-Date $p.LatestTime -Format "yyyy-MM-dd"
        Write-Output "  $($p.Name) | card=$c latest=$l"
    }
    Write-Output ""
}

if ($NoCardProjects.Count -gt 0) {
    Write-Output "NO CARD ($($NoCardProjects.Count) projects)"
    foreach ($name in $NoCardProjects) {
        Write-Output "  - $name  ->  missing $CardRelative"
    }
    Write-Output ""
}

if ($NoOtherFilesProjects.Count -gt 0) {
    Write-Output "NO FILES ($($NoOtherFilesProjects.Count) projects, card only)"
    foreach ($name in $NoOtherFilesProjects) {
        Write-Output "  - $name"
    }
    Write-Output ""
}

$totalChecked = $DriftProjects.Count + $OkProjects.Count + $NoCardProjects.Count + $NoOtherFilesProjects.Count
Write-Output "Scanned $totalChecked projects, $($DriftProjects.Count) need card update."

if ($DriftProjects.Count -gt 0 -or $NoCardProjects.Count -gt 0) {
    exit 1
}
exit 0