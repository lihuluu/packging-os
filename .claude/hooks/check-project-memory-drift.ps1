$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$projectsRoot = Join-Path $root "Workspace\Projects"

if (-not (Test-Path $projectsRoot)) {
    exit 0
}

$ignoredNames = @(
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
    ".gitkeep",
    ".gitignore"
)

$drifted = @()

foreach ($project in Get-ChildItem -LiteralPath $projectsRoot -Directory) {
    $card = Join-Path $project.FullName "00_Project_Control\project-memory-card.md"

    $latest = Get-ChildItem -LiteralPath $project.FullName -Recurse -File |
        Where-Object {
            $_.FullName -notlike "*\00_Project_Control\*" -and
            $_.Name -notlike "*.tmp.*" -and
            $ignoredNames -notcontains $_.Name
        } |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1

    if (-not $latest) {
        continue
    }

    if (-not (Test-Path $card)) {
        $drifted += [PSCustomObject]@{
            Project = $project.Name
            Status = "missing card"
            CardTime = ""
            LatestTime = $latest.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
            LatestFile = $latest.FullName.Substring($project.FullName.Length + 1)
        }
        continue
    }

    $cardItem = Get-Item -LiteralPath $card
    if ($latest.LastWriteTime -gt $cardItem.LastWriteTime.AddMinutes(1)) {
        $drifted += [PSCustomObject]@{
            Project = $project.Name
            Status = "card may be stale"
            CardTime = $cardItem.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
            LatestTime = $latest.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
            LatestFile = $latest.FullName.Substring($project.FullName.Length + 1)
        }
    }
}

if ($drifted.Count -eq 0) {
    exit 0
}

Write-Output "<packging-os-reminder>"
Write-Output "Some project memory cards may be behind the latest project files. If the user request touches project status, project memory, dashboards, or handoff state, consider reminding them or updating the relevant card explicitly."

foreach ($item in ($drifted | Select-Object -First 5)) {
    Write-Output ("- {0}: {1}; card={2}; latest={3}; latest_file={4}" -f $item.Project, $item.Status, $item.CardTime, $item.LatestTime, $item.LatestFile)
}

if ($drifted.Count -gt 5) {
    Write-Output ("- ... plus {0} more project(s)." -f ($drifted.Count - 5))
}

Write-Output "</packging-os-reminder>"
exit 0
