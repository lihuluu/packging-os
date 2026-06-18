param(
    [string]$KnowledgeRoot = "",
    [string]$CoverageScript = "",
    [string]$PacketScript = ""
)

$repoRoot = Join-Path $PSScriptRoot "..\..\..\.."
. (Join-Path $PSScriptRoot "knowledge-file-utils.ps1")

if ([string]::IsNullOrWhiteSpace($KnowledgeRoot)) {
    $KnowledgeRoot = Join-Path $repoRoot "Workspace\Knowledge\Operations"
}

if ([string]::IsNullOrWhiteSpace($CoverageScript)) {
    $CoverageScript = Join-Path $PSScriptRoot "get-knowledge-coverage.ps1"
}

if ([string]::IsNullOrWhiteSpace($PacketScript)) {
    $PacketScript = Join-Path $PSScriptRoot "build-knowledge-review-packet.ps1"
}

$coveragePath = Join-Path $KnowledgeRoot "coverage\project-knowledge-coverage.md"
$inboxPath = Join-Path $KnowledgeRoot "queue\knowledge-capture-inbox.md"
$reviewPacketPath = Join-Path $KnowledgeRoot "current\current-review-session.md"
$draftLogPath = Join-Path $KnowledgeRoot "current\current-review-log-draft.md"

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

function Get-NextAction {
    param([string]$Status)

    switch ($Status) {
        "Missing Synthesis" { return "Create or update project-level knowledge-synthesis.md, then write back shared knowledge." }
        "Synthesis Created" { return "Keep the synthesis in sync when supplier feedback, validation results, or a retrospective is added." }
        "Ready" { return "Confirm the project has enough review signal, then start a knowledge-synthesis draft." }
        "Low Signal" { return "Keep collecting stage outputs before extracting shared knowledge." }
        default { return "Track only if the project changes again." }
    }
}

function Join-ProjectList {
    param([object[]]$Items)

    if ($null -eq $Items -or $Items.Count -eq 0) {
        return "none"
    }

    return ($Items -join ", ")
}

if (-not (Test-Path $KnowledgeRoot)) {
    New-Item -ItemType Directory -Path $KnowledgeRoot | Out-Null
}

$coverageRaw = & $CoverageScript
$coverageJson = ($coverageRaw | Out-String)
$coverageParsed = ConvertFrom-Json -InputObject $coverageJson
$coverageRows = @($coverageParsed)
[void](& $PacketScript)

$coverageLines = @(
    "# Project Knowledge Coverage",
    "",
    "## Status Definitions",
    "",
    "- `Done`: project-level knowledge capture exists.",
    "- `Synthesis Created`: `knowledge-synthesis.md` exists, but the project is still active or waiting for a retrospective update.",
    "- `Missing Synthesis`: the project has enough output or a retrospective, but no `knowledge-synthesis.md` yet.",
    "- `Ready`: the project looks mature enough to start knowledge capture.",
    "- `Low Signal`: not enough project output yet.",
    "",
    "## Coverage Table",
    "",
    "| Project | Status | Memory Card | Retrospective | Knowledge Synthesis | Doc Count | Last Updated |",
    "| --- | --- | --- | --- | --- | --- | --- |"
)

foreach ($row in $coverageRows) {
    $memoryCard = if ($row.HasMemoryCard) { "Yes" } else { "No" }
    $retrospective = if ($row.HasRetrospective) { "Yes" } else { "No" }
    $synthesis = if ($row.HasKnowledgeSynthesis) { "Yes" } else { "No" }
    $coverageLines += "| $($row.Project) | $($row.Status) | $memoryCard | $retrospective | $synthesis | $($row.DocumentCount) | $($row.LastUpdated) |"
}

$coverageLines += ""
$coverageLines += "## Next Actions"
$coverageLines += ""
$coverageLines += "- New projects should create `project-memory-card.md` first."
$coverageLines += "- Projects with a retrospective but no `knowledge-synthesis.md` should enter the next review pass."

Write-KnowledgeFileAtomic -Path $coveragePath -Lines $coverageLines

$activeRows = @($coverageRows | Where-Object { $_.Status -ne "Done" } | ForEach-Object {
    [PSCustomObject]@{
        Project = $_.Project
        Status = $_.Status
        Priority = Get-Priority -Status $_.Status
        NextAction = Get-NextAction -Status $_.Status
        LastUpdated = $_.LastUpdated
    }
})

$priorityOrder = @{ P1 = 1; P2 = 2; P3 = 3; Done = 4 }
$activeRows = @($activeRows | Sort-Object @{ Expression = { $priorityOrder[$_.Priority] } }, @{ Expression = { $_.Project } })

$inboxLines = @(
    "# Knowledge Capture Inbox",
    "",
    "## Purpose",
    "",
    "This file tracks projects or observations that should be turned into reusable knowledge but are not finished yet.",
    "",
    "Rules:",
    "- Keep only active items here.",
    "- Remove items after they are handled.",
    "- If an observation is low confidence, write how it should be validated.",
    "",
    "## Current Queue",
    ""
)

if ($activeRows.Count -eq 0) {
    $inboxLines += "- none"
} else {
    foreach ($row in $activeRows) {
        $inboxLines += "### $($row.Priority) - $($row.Project)"
        $inboxLines += "- Status: $($row.Status)"
        $inboxLines += "- Last Updated: $($row.LastUpdated)"
        $inboxLines += "- Suggested Action: $($row.NextAction)"
        $inboxLines += ""
    }
}

Write-KnowledgeFileAtomic -Path $inboxPath -Lines $inboxLines

$today = Get-Date -Format "yyyy-MM-dd"
$p1Projects = @($activeRows | Where-Object { $_.Priority -eq "P1" } | Select-Object -ExpandProperty Project)
$p2Projects = @($activeRows | Where-Object { $_.Priority -eq "P2" } | Select-Object -ExpandProperty Project)
$p3Projects = @($activeRows | Where-Object { $_.Priority -eq "P3" } | Select-Object -ExpandProperty Project)

$draftLines = @(
    "# Current Review Log Draft",
    "",
    "## Session Info",
    ('- Date: {0}' -f $today),
    '- Trigger: `.claude/skills/knowledge-synthesizer/scripts/start-knowledge-review-session.ps1`',
    ('- Projects Scanned: {0}' -f $coverageRows.Count),
    ('- Projects Needing Attention: {0}' -f $activeRows.Count),
    "",
    "## Current Priority Queue",
    "- P1: $(Join-ProjectList -Items $p1Projects)",
    "- P2: $(Join-ProjectList -Items $p2Projects)",
    "- P3: $(Join-ProjectList -Items $p3Projects)",
    "",
    "## Planned Actions",
    "1. Handle all P1 projects first.",
    "2. Then cover P2 projects that are ready for synthesis.",
    "3. Update the workspace digest and finalize the history log.",
    "",
    "## Findings During The Session",
    "- ",
    "",
    "## Before Finalizing The History Log",
    "- [ ] `workspace-knowledge-digest.md` is updated",
    "- [ ] completed inbox items are removed",
    "- [ ] project-level synthesis files were reviewed"
)

$draftDir = Split-Path -Parent $draftLogPath
if (-not (Test-Path $draftDir)) {
    New-Item -ItemType Directory -Path $draftDir | Out-Null
}

Write-KnowledgeFileAtomic -Path $draftLogPath -Lines $draftLines

[PSCustomObject]@{
    CoveragePath = $coveragePath
    InboxPath = $inboxPath
    ReviewPacketPath = $reviewPacketPath
    DraftLogPath = $draftLogPath
    ProjectsScanned = $coverageRows.Count
    ProjectsNeedingAttention = $activeRows.Count
} | ConvertTo-Json -Depth 3
