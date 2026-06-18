param(
    [string]$OutputPath = ""
)

# Scripts now live inside the skill folder, so resolve the repo root first.
$repoRoot = Join-Path $PSScriptRoot "..\..\..\.."
. (Join-Path $PSScriptRoot "knowledge-file-utils.ps1")
$projectsRoot = Join-Path $repoRoot "Workspace\Projects"
$knowledgeRoot = Join-Path $repoRoot "Workspace\Knowledge\Operations"

if (-not (Test-Path $projectsRoot)) {
    Write-Error "Projects directory not found: $projectsRoot"
    exit 1
}

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $knowledgeRoot "current\current-review-session.md"
}

$projectDirs = Get-ChildItem -Path $projectsRoot -Directory | Where-Object { $_.Name -notlike "_*" }

function Test-IsOperationalNoise {
    param([System.IO.FileInfo]$File)

    if ($null -eq $File) { return $true }
    if ($File.Name -eq ".DS_Store") { return $true }
    if ($File.Name -match "\.tmp\.\d+\.\d+$") { return $true }
    return $false
}

function Get-ProjectFiles {
    param([string]$ProjectPath)

    Get-ChildItem -Path $ProjectPath -Recurse -File |
        Where-Object { -not (Test-IsOperationalNoise -File $_) }
}

function Get-ProjectStatus {
    param([string]$ProjectPath)

    $retroPath = Join-Path $ProjectPath "05_Retrospective\project-retrospective.md"
    $synthesisPath = Join-Path $ProjectPath "05_Retrospective\knowledge-synthesis.md"
    $memoryPath = Join-Path $ProjectPath "00_Project_Control\project-memory-card.md"
    $docCount = @((Get-ProjectFiles -ProjectPath $ProjectPath)).Count

    if (Test-Path $synthesisPath) {
        if (Test-Path $retroPath) { return "Done" }
        return "Synthesis Created"
    }
    if (Test-Path $retroPath) { return "Missing Synthesis" }
    if ($docCount -ge 4 -and (Test-Path $memoryPath)) { return "Ready" }
    return "Low Signal"
}

function Get-Priority {
    param([string]$Status)
    switch ($Status) {
        "Missing Synthesis" { return "P1" }
        "Synthesis Created" { return "P2" }
        "Ready" { return "P2" }
        "Low Signal" { return "P3" }
        default { return "Done" }
    }
}

$rows = foreach ($project in $projectDirs) {
    $status = Get-ProjectStatus -ProjectPath $project.FullName
    $priority = Get-Priority -Status $status

    $recentFiles = Get-ProjectFiles -ProjectPath $project.FullName |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 5

    $recommendedSources = @()
    foreach ($file in $recentFiles) {
        $relativePath = $file.FullName.Replace((Resolve-Path $projectsRoot).Path + "\", "")
        $recommendedSources += $relativePath
    }

    [PSCustomObject]@{
        Project = $project.Name
        Status = $status
        Priority = $priority
        RecommendedSources = $recommendedSources
        LastUpdated = ($recentFiles | Select-Object -First 1).LastWriteTime
    }
}

$sortedRows = @($rows | Sort-Object `
    @{ Expression = { switch ($_.Priority) { "P1" { 1 } "P2" { 2 } "P3" { 3 } default { 4 } } } }, `
    @{ Expression = { $_.Project } })

$scanDate = Get-Date -Format "yyyy-MM-dd HH:mm"
$activeRows = @($sortedRows | Where-Object { $_.Priority -ne "Done" })

$lines = @()
$lines += "# Current Knowledge Review Session"
$lines += ""
$lines += "## Session Metadata"
$lines += "- Generated At: $scanDate"
$lines += "- Projects Scanned: $($sortedRows.Count)"
$lines += "- Projects Needing Attention: $($activeRows.Count)"
$lines += ""
$lines += "## Priority Queue"
$lines += ""
$lines += "| Project | Priority | Status | Latest Activity |"
$lines += "| --- | --- | --- | --- |"

foreach ($row in $sortedRows) {
    $lastUpdated = if ($row.LastUpdated) { $row.LastUpdated.ToString("yyyy-MM-dd HH:mm") } else { "" }
    $lines += "| $($row.Project) | $($row.Priority) | $($row.Status) | $lastUpdated |"
}

$lines += ""
$lines += "## Recommended Review Order"
$lines += ""

if ($activeRows.Count -eq 0) {
    $lines += "- No active projects require knowledge capture right now."
} else {
    foreach ($row in $activeRows) {
        $lines += "### $($row.Priority) - $($row.Project)"
        $lines += "- Status: $($row.Status)"
        $lines += "- Suggested files:"
        foreach ($source in $row.RecommendedSources) {
            $lines += "  - $source"
        }
        $lines += ""
    }
}

$lines += ""
$lines += "## Session Checklist"
$lines += ""
$lines += '1. Update `coverage/project-knowledge-coverage.md` if statuses changed.'
$lines += '2. Add missing projects to `queue/knowledge-capture-inbox.md`.'
$lines += '3. Complete project-level `knowledge-synthesis.md` for P1/P2 projects.'
$lines += '4. Update `workspace-knowledge-digest.md` with this round''s changes.'
$lines += '5. Write a history entry under `Workspace/Knowledge/Operations/history/`.'

$directory = Split-Path -Parent $OutputPath
if (-not (Test-Path $directory)) {
    New-Item -ItemType Directory -Path $directory | Out-Null
}

Write-KnowledgeFileAtomic -Path $OutputPath -Lines $lines
Get-Item $OutputPath | Select-Object FullName, LastWriteTime
