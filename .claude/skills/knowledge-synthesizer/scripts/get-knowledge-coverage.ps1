$repoRoot = Join-Path $PSScriptRoot "..\..\..\.."
$projectsRoot = Join-Path $repoRoot "Workspace\Projects"

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

if (-not (Test-Path $projectsRoot)) {
    Write-Error "Projects directory not found: $projectsRoot"
    exit 1
}

$projectDirs = Get-ChildItem -Path $projectsRoot -Directory | Where-Object { $_.Name -notlike "_*" }

$rows = foreach ($project in $projectDirs) {
    $retroPath = Join-Path $project.FullName "05_Retrospective\project-retrospective.md"
    $synthesisPath = Join-Path $project.FullName "05_Retrospective\knowledge-synthesis.md"
    $memoryPath = Join-Path $project.FullName "00_Project_Control\project-memory-card.md"
    $projectFiles = @(Get-ProjectFiles -ProjectPath $project.FullName)
    $docCount = ($projectFiles | Measure-Object).Count

    $status = if (Test-Path $synthesisPath) {
        if (Test-Path $retroPath) { "Done" } else { "Synthesis Created" }
    } elseif (Test-Path $retroPath) {
        "Missing Synthesis"
    } elseif ($docCount -ge 4 -and (Test-Path $memoryPath)) {
        "Ready"
    } else {
        "Low Signal"
    }

    $lastUpdated = ($projectFiles |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1).LastWriteTime

    [PSCustomObject]@{
        Project = $project.Name
        Status = $status
        HasMemoryCard = Test-Path $memoryPath
        HasRetrospective = Test-Path $retroPath
        HasKnowledgeSynthesis = Test-Path $synthesisPath
        DocumentCount = $docCount
        LastUpdated = if ($lastUpdated) { $lastUpdated.ToString("yyyy-MM-dd HH:mm") } else { "" }
    }
}

$rows | Sort-Object Status, Project | ConvertTo-Json -Depth 3
