# init-project.ps1 - Packging OS project directory initialization (PowerShell)
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File init-project.ps1 "Project Name"
#   powershell -ExecutionPolicy Bypass -File init-project.ps1 "Project Name" -DryRun
#
# Creates standard directory structure and starter files under Workspace/Projects/.

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$ProjectName,
    [string]$Root,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

if (-not $Root) {
    $Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")).Path
}
$Root = (Resolve-Path $Root).Path

$Dirs = @(
    "00_Project_Control",
    "01_Brief",
    "02_Research",
    "03_Design\01_Working",
    "03_Design\02_Assets",
    "03_Design\02_Assets\AI_Concepts",
    "03_Design\03_Presentation",
    "03_Design\04_Production",
    "03_Design\05_Renders",
    "03_Design\06_Proof_Record",
    "04_Final\01_Print_Files",
    "04_Final\02_Source_Files",
    "04_Final\03_Assets",
    "04_Final\04_Previews",
    "04_Final\05_Dielines",
    "05_Retrospective"
)

$StarterFiles = @(
    @{ Template = ".claude\skills\project-memory-manager\assets\project-memory-card-template.md"; Dest = "00_Project_Control\project-memory-card.md" },
    @{ Template = ".claude\skills\project-tracker\assets\project-tracker-template.md";           Dest = "00_Project_Control\project-tracker.md" },
    @{ Template = ".claude\skills\visual-system-builder\assets\asset-register-template.md";       Dest = "03_Design\02_Assets\asset-register.md" },
    @{ Template = ".claude\skills\supplier-brief-writer\assets\supplier-brief-template.md";      Dest = "03_Design\04_Production\supplier-brief.md" },
    @{ Template = ".claude\skills\prepress-checker\assets\compliance-review-template.md";        Dest = "03_Design\06_Proof_Record\compliance-review.md" },
    @{ Template = ".claude\skills\prepress-checker\assets\sample-acceptance-record-template.md"; Dest = "03_Design\06_Proof_Record\sample-acceptance-record.md" },
    @{ Template = ".claude\skills\prepress-checker\assets\proofing-record-template.md";          Dest = "03_Design\06_Proof_Record\proofing-record.md" },
    @{ Template = ".claude\skills\brief-decomposer\assets\brief-decomposition-template.md";       Dest = "01_Brief\brief-decomposition.md" },
    @{ Template = ".claude\skills\brief-decomposer\assets\packaging-brief-template.md";           Dest = "01_Brief\packaging-brief.md" },
    @{ Template = ".claude\skills\design-version-tracker\assets\decision-log-template.md";        Dest = "03_Design\01_Working\decision-log.md" }
)

$ProjectDir = Join-Path $Root "Workspace\Projects\$ProjectName"

if (Test-Path $ProjectDir) {
    Write-Error "Directory already exists: $ProjectDir"
    Write-Error "Delete or rename the existing directory first."
    exit 1
}

Write-Output "Project root: $ProjectDir"
Write-Output "Mode: $(if ($DryRun) {'dry-run (no files created)'} else {'live'})"
Write-Output ""

# Create directories
foreach ($rel in $Dirs) {
    $target = Join-Path $ProjectDir $rel
    $display = $target.Substring($Root.Length + 1)
    Write-Output "  mkdir  $display"
    if (-not $DryRun) {
        New-Item -ItemType Directory -Path $target -Force | Out-Null
    }
}

# Write starter files from templates
foreach ($sf in $StarterFiles) {
    $templatePath = Join-Path $Root $sf.Template
    $destPath = Join-Path $ProjectDir $sf.Dest
    $display = $destPath.Substring($Root.Length + 1)

    if (-not (Test-Path $templatePath)) {
        Write-Output "  SKIP   $display (template missing: $($sf.Template))"
        continue
    }

    $content = [System.IO.File]::ReadAllText($templatePath, [System.Text.UTF8Encoding]::new($false))

    # Inject project name into first occurrence
    $marker = "- `u{9879}`u{76EE}`u{540D}`u{79F0}`u{FF1A}"
    $replacement = "- `u{9879}`u{76EE}`u{540D}`u{79F0}`u{FF1A}$ProjectName"
    $idx = $content.IndexOf($marker)
    if ($idx -ge 0) {
        $content = $content.Remove($idx, $marker.Length).Insert($idx, $replacement)
    }

    Write-Output "  write  $display"
    if (-not $DryRun) {
        [System.IO.File]::WriteAllText($destPath, $content, [System.Text.UTF8Encoding]::new($false))
    }
}

Write-Output ""
if ($DryRun) {
    Write-Output "dry-run complete, no files created."
}
else {
    Write-Output "Project initialized: $ProjectName"
    Write-Output "Starter files:"
    Write-Output "- 00_Project_Control/project-memory-card.md"
    Write-Output "- 00_Project_Control/project-tracker.md"
    Write-Output "- 03_Design/02_Assets/asset-register.md"
    Write-Output "- 03_Design/02_Assets/AI_Concepts/"
    Write-Output "- 03_Design/04_Production/supplier-brief.md"
    Write-Output "- 03_Design/06_Proof_Record/compliance-review.md"
    Write-Output "- 03_Design/06_Proof_Record/sample-acceptance-record.md"
    Write-Output "- 03_Design/06_Proof_Record/proofing-record.md"
    Write-Output "- 03_Design/01_Working/decision-log.md"
    Write-Output "- 01_Brief/brief-decomposition.md"
    Write-Output "- 01_Brief/packaging-brief.md"

    Write-Output "Next: fill in project card and brief, then run packging-os."
}
