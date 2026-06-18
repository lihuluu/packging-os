#requires -version 5.1
# validate-packging-os.ps1 - Packging OS governance validation (cross-platform)
# Works on Windows PowerShell 5.1+ and PowerShell Core 7+ (Mac/Linux)
param(
    [string]$Root
)

if (-not $Root) {
    $Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")).Path
}

$ErrorActionPreference = "Stop"
$ScriptDir = $PSScriptRoot

# Load headings from shared config (UTF-8 JSON file)
$ConfigPath = Join-Path $ScriptDir "validation-config.json"
if (-not (Test-Path $ConfigPath)) {
    Write-Host "[fatal] Missing validation-config.json in $ScriptDir" -ForegroundColor Red
    exit 2
}
$ConfigBytes = [System.IO.File]::ReadAllBytes($ConfigPath)
$ConfigJson = [System.Text.Encoding]::UTF8.GetString($ConfigBytes)
$Config = ConvertFrom-Json $ConfigJson

$projectMemoryHeadings = $Config.projectMemoryHeadings
$retrospectiveHeadings = $Config.retrospectiveHeadings
$knowledgeHeadings = $Config.knowledgeHeadings
$decisionLogHeadings = $Config.decisionLogHeadings

$issues = New-Object System.Collections.Generic.List[string]

# --- Settings ---
$tempFilePatterns = @(".DS_Store", "Thumbs.db", "desktop.ini")
$textScanSuffixes = @(".md", ".py", ".ps1", ".sh", ".cmd")
$legacyFilenames = @{
    "project_tracker.md" = "project-tracker.md"
    "structure-selection.md" = "structure-decision.md"
}
$legacyPathSegments = @{
    "03_Design/02_Structure/" = "03_Design/04_Production/"
}
$legacyTextPatterns = [ordered]@{
    "packaging-os-maintainer" = "packging-os-maintainer"
    "packaging-os" = "packging-os"
    "validate-design-os" = "validate-packging-os"
    "Design OS" = "Packging OS"
    "design-os" = "packging-os"
    "Packaging OS" = "Packging OS"
    "Packaging Design OS" = "Packging OS"
}
$oldRootPatterns = @(
    "/Users/lihulu/Library/CloudStorage/Dropbox/Design_OS"
    "/Users/lihulu/Documents/Packgaing_Design"
)

# --- Helpers ---
function Add-Issue {
    param([string]$Message)
    $issues.Add($Message)
}

function Get-DisplayPath {
    param([string]$FilePath)
    if ($FilePath.StartsWith($Root)) {
        return ($FilePath.Substring($Root.Length + 1) -replace "\\", "/")
    }
    return ($FilePath -replace "\\", "/")
}

function Read-FileAsUtf8 {
    param([string]$FilePath)
    $bytes = [System.IO.File]::ReadAllBytes($FilePath)
    return [System.Text.Encoding]::UTF8.GetString($bytes)
}

# --- Check functions ---
function Test-MarkdownLinks {
    param(
        [string]$BasePath,
        [string]$DisplayPath
    )
    $content = Read-FileAsUtf8 $BasePath
    $matches = [regex]::Matches($content, '\]\(((?:\./|\.\./)[^)#?]+)\)')
    foreach ($m in $matches) {
        $link = $m.Groups[1].Value
        $target = Join-Path (Split-Path -Parent $BasePath) $link
        $resolved = if (Test-Path $target) { (Resolve-Path $target).Path } else { $null }
        if (-not $resolved) {
            Add-Issue "[broken-link] $DisplayPath -> $link"
        }
    }
}

function Test-RequiredHeadings {
    param(
        [string]$TemplatePath,
        [string[]]$Headings
    )
    if (-not (Test-Path $TemplatePath)) {
        Add-Issue "[missing-template] $(Get-DisplayPath $TemplatePath)"
        return
    }
    $content = Read-FileAsUtf8 $TemplatePath
    foreach ($heading in $Headings) {
        if ($content -notmatch [regex]::Escape($heading)) {
            $displayHeading = $heading -replace '^## ', ''
            Add-Issue "[missing-heading] '$displayHeading' in $(Get-DisplayPath $TemplatePath)"
        }
    }
}

function Test-ProjectDocHeadings {
    param(
        [string]$ProjectRoot,
        [string]$Filename,
        [string[]]$Headings
    )
    if (-not (Test-Path $ProjectRoot)) { return }
    Get-ChildItem -Path $ProjectRoot -Recurse -Filter $Filename -File | ForEach-Object {
        $content = Read-FileAsUtf8 $_.FullName
        foreach ($heading in $Headings) {
            if ($content -notmatch [regex]::Escape($heading)) {
                $displayHeading = $heading -replace '^## ', ''
                Add-Issue "[missing-heading] '$displayHeading' in $(Get-DisplayPath $_.FullName)"
            }
        }
    }
}

function Test-TempFiles {
    Get-ChildItem -Path $Root -Recurse -Force | ForEach-Object {
        if ($_.PSIsContainer) {
            if ($_.Name -eq "__pycache__") {
                Add-Issue "[temp-dir] $(Get-DisplayPath $_.FullName)"
            }
            return
        }
        $isTemp = $false
        if ($tempFilePatterns -contains $_.Name) { $isTemp = $true }
        if ($_.Name.StartsWith("~$")) { $isTemp = $true }
        if ($_.Name.EndsWith(".tmp")) { $isTemp = $true }
        if ($_.Name.Contains(".tmp.")) { $isTemp = $true }
        if ($_.Name.EndsWith(".bak")) { $isTemp = $true }
        if ($_.Name.EndsWith(".log")) { $isTemp = $true }
        if ($_.Name -eq ".gitkeep" -and $_.Length -eq 0) { $isTemp = $true }
        if ($isTemp) {
            Add-Issue "[temp-file] $(Get-DisplayPath $_.FullName)"
        }
    }
}

# Dashboard retired - no longer checked

function Test-LegacyFilenames {
    param([string]$ProjectRoot)
    if (-not (Test-Path $ProjectRoot)) { return }
    Get-ChildItem -Path $ProjectRoot -Recurse -File | ForEach-Object {
        if ($legacyFilenames.ContainsKey($_.Name)) {
            Add-Issue "[legacy-filename] $(Get-DisplayPath $_.FullName) -> should be $($legacyFilenames[$_.Name])"
        }
    }
}

function Test-LegacyPathReferences {
    param([string[]]$ScanRoots)
    foreach ($scanRoot in $ScanRoots) {
        if (-not (Test-Path $scanRoot)) { continue }
        Get-ChildItem -Path $scanRoot -Recurse -Filter "*.md" -File | ForEach-Object {
            $content = Read-FileAsUtf8 $_.FullName
            foreach ($legacyPath in $legacyPathSegments.Keys) {
                if ($content.Contains($legacyPath)) {
                    Add-Issue "[legacy-path] $(Get-DisplayPath $_.FullName) -> '$legacyPath' should be '$($legacyPathSegments[$legacyPath])'"
                }
            }
        }
    }
}

function Test-LegacyTextReferences {
    Get-ChildItem -Path $Root -Recurse -File | ForEach-Object {
        if ($textScanSuffixes -notcontains $_.Extension) { return }
        if ($_.Name -in @("validate-packging-os.py", "validate-packging-os.ps1")) { return }
        $content = Read-FileAsUtf8 $_.FullName
        $displayPath = Get-DisplayPath $_.FullName
        foreach ($legacyText in $legacyTextPatterns.Keys) {
            if ($content.Contains($legacyText)) {
                Add-Issue "[legacy-name] $displayPath -> '$legacyText' should be '$($legacyTextPatterns[$legacyText])'"
            }
        }
        foreach ($oldRoot in $oldRootPatterns) {
            if ($content.Contains($oldRoot)) {
                Add-Issue "[old-root-path] $displayPath -> $oldRoot"
            }
        }
    }
}

function Test-DecisionLogIds {
    param(
        [string]$Path,
        [switch]$AllowPlaceholder
    )
    if (-not (Test-Path $Path)) {
        Add-Issue "[missing-template] $(Get-DisplayPath $Path)"
        return
    }

    $inDecisionTable = $false
    $lineNumber = 0
    foreach ($line in (Read-FileAsUtf8 $Path) -split "`r?`n") {
        $lineNumber += 1
        $stripped = $line.Trim()
        if ($stripped.StartsWith("| 缂栧彿 |")) {
            $inDecisionTable = $true
            continue
        }
        if (-not $inDecisionTable) { continue }
        if (-not $stripped.StartsWith("|")) {
            if (-not [string]::IsNullOrWhiteSpace($stripped)) {
                $inDecisionTable = $false
            }
            continue
        }

        $parts = $stripped.Trim("|").Split("|") | ForEach-Object { $_.Trim() }
        if ($parts.Count -eq 0) { continue }
        $firstCell = $parts[0]
        if ([string]::IsNullOrWhiteSpace($firstCell) -or $firstCell -match "^-+$") { continue }
        if ($AllowPlaceholder -and $firstCell -eq "D-___") { continue }
        if ($firstCell -notmatch "^D-\d{3}$") {
            Add-Issue "[decision-id-format] $(Get-DisplayPath $Path):$lineNumber -> first column should be D-NNN, got '$firstCell'"
        }
    }
}

function Test-ProjectDecisionLogIds {
    param([string]$ProjectRoot)
    if (-not (Test-Path $ProjectRoot)) { return }
    Get-ChildItem -Path $ProjectRoot -Recurse -File -Filter "decision-log.md" | ForEach-Object {
        Test-DecisionLogIds -Path $_.FullName -AllowPlaceholder
    }
}

function Get-MarkdownTableFirstColumn {
    param([string]$Path)
    $entries = New-Object System.Collections.Generic.HashSet[string]
    foreach ($line in (Read-FileAsUtf8 $Path) -split "`r?`n") {
        $stripped = $line.Trim()
        if (-not $stripped.StartsWith("|")) { continue }
        $parts = $stripped.Trim("|").Split("|") | ForEach-Object { $_.Trim() }
        if ($parts.Count -lt 2) { continue }
        $firstCell = $parts[0]
        if ($firstCell -eq "Project" -or $firstCell -eq "---" -or [string]::IsNullOrEmpty($firstCell)) { continue }
        [void]$entries.Add($firstCell)
    }
    return $entries
}

function Test-CoverageSync {
    $projectsDir = Join-Path $Root "Workspace/Projects"
    if (-not (Test-Path $projectsDir)) { return }

    $projectNames = @()
    Get-ChildItem -Path $projectsDir -Directory | ForEach-Object {
        if (-not $_.Name.StartsWith(".")) {
            $projectNames += $_.Name
        }
    }

    $coverageFile = Join-Path $Root "Workspace/Knowledge/Operations/coverage/project-knowledge-coverage.md"
    if (Test-Path $coverageFile) {
        $coverageProjects = Get-MarkdownTableFirstColumn -Path $coverageFile
        foreach ($name in $projectNames) {
            if (-not $coverageProjects.Contains($name)) {
                Add-Issue "[coverage-missing] $(Get-DisplayPath $coverageFile) -> missing project: $name"
            }
        }
        foreach ($name in ($coverageProjects | Sort-Object)) {
            if ($projectNames -notcontains $name) {
                Add-Issue "[coverage-unknown] $(Get-DisplayPath $coverageFile) -> unknown project: $name"
            }
        }
    }

    $sessionFile = Join-Path $Root "Workspace/Knowledge/Operations/current/current-review-session.md"
    if (Test-Path $sessionFile) {
        $sessionProjects = Get-MarkdownTableFirstColumn -Path $sessionFile
        foreach ($name in $projectNames) {
            if (-not $sessionProjects.Contains($name)) {
                Add-Issue "[session-missing] $(Get-DisplayPath $sessionFile) -> missing project: $name"
            }
        }
        foreach ($name in ($sessionProjects | Sort-Object)) {
            if ($projectNames -notcontains $name -and $name -ne "Done") {
                Add-Issue "[session-unknown] $(Get-DisplayPath $sessionFile) -> unknown project: $name"
            }
        }
    }

    $logDraftFile = Join-Path $Root "Workspace/Knowledge/Operations/current/current-review-log-draft.md"
    if (Test-Path $logDraftFile) {
        foreach ($line in (Read-FileAsUtf8 $logDraftFile) -split "`r?`n") {
            $stripped = $line.Trim()
            if ($stripped -notmatch "^- P\d+:") { continue }
            $value = $stripped.Substring($stripped.IndexOf(":") + 1)
            foreach ($chunk in $value.Split(",")) {
                $projectName = $chunk.Trim()
                if ([string]::IsNullOrEmpty($projectName) -or $projectName.ToLower() -eq "none") { continue }
                if ($projectNames -notcontains $projectName) {
                    Add-Issue "[log-draft-unknown] $(Get-DisplayPath $logDraftFile) -> unknown project: $projectName"
                }
            }
        }
    }
}

# --- Main execution ---

# 1. Required root docs
$requiredDocs = @("README.md", "CLAUDE.md", ".claude/references/skills-test-cases.md")
foreach ($doc in $requiredDocs) {
    if (-not (Test-Path (Join-Path $Root $doc))) {
        Add-Issue "[missing-doc] $doc"
    }
}

# 2. Skill root
$skillRoot = Join-Path $Root ".claude/skills"
if (-not (Test-Path $skillRoot)) {
    Add-Issue "[missing-dir] .claude/skills"
}

# 3. Shared glossary
$sharedGlossary = Join-Path $Root ".claude/references/shared-field-glossary.md"
if (-not (Test-Path $sharedGlossary)) {
    Add-Issue "[missing-glossary] .claude/references/shared-field-glossary.md"
}

# 4. Skill SKILL.md + markdown links
$skillDirs = @()
if (Test-Path $skillRoot) {
    $skillDirs = Get-ChildItem -Path $skillRoot -Directory | Sort-Object Name
    foreach ($dir in $skillDirs) {
        $skillMd = Join-Path $dir.FullName "SKILL.md"
        if (-not (Test-Path $skillMd)) {
            Add-Issue "[missing-skill-md] $($dir.Name)"
            continue
        }
        Test-MarkdownLinks -BasePath $skillMd -DisplayPath (Get-DisplayPath $skillMd)
        Get-ChildItem -Path $dir.FullName -Recurse -Filter "*.md" -File | ForEach-Object {
            Test-MarkdownLinks -BasePath $_.FullName -DisplayPath (Get-DisplayPath $_.FullName)
        }
    }
}

# 5. README skill table sync
$readme = Join-Path $Root "README.md"
if (Test-Path $readme) {
    $readmeContent = Read-FileAsUtf8 $readme
    $readmeSkills = [regex]::Matches($readmeContent, '\|\s*`([^`]+)`\s*\|') | ForEach-Object {
        $_.Groups[1].Value
    } | Sort-Object -Unique
    foreach ($skill in ($skillDirs.Name | Sort-Object -Unique)) {
        if ($readmeSkills -notcontains $skill) {
            Add-Issue "[readme-missing-skill] $skill"
        }
    }
}

# 6. packging-os router sync
$packagingSkill = Join-Path $skillRoot "packging-os/SKILL.md"
$packagingScopeExclusions = @("packging-os", "packging-os-maintainer")
if (Test-Path $packagingSkill) {
    $packagingContent = Read-FileAsUtf8 $packagingSkill
    foreach ($skill in ($skillDirs.Name | Where-Object { $packagingScopeExclusions -notcontains $_ })) {
        $skillToken = '`' + $skill + '`'
        if ($packagingContent -notmatch [regex]::Escape($skillToken)) {
            Add-Issue "[router-missing-skill] packging-os does not reference: $skill"
        }
    }
}

# 7. Template headings
$projectMemoryTemplate = Join-Path $skillRoot "project-memory-manager/assets/project-memory-card-template.md"
$retrospectiveTemplate = Join-Path $skillRoot "project-retrospective/assets/project-retrospective-template.md"
$knowledgeTemplate = Join-Path $skillRoot "knowledge-synthesizer/assets/knowledge-synthesis-template.md"
$decisionLogTemplate = Join-Path $skillRoot "design-version-tracker/assets/decision-log-template.md"

Test-RequiredHeadings -TemplatePath $projectMemoryTemplate -Headings $projectMemoryHeadings
Test-RequiredHeadings -TemplatePath $retrospectiveTemplate -Headings $retrospectiveHeadings
Test-RequiredHeadings -TemplatePath $knowledgeTemplate -Headings $knowledgeHeadings
Test-RequiredHeadings -TemplatePath $decisionLogTemplate -Headings $decisionLogHeadings
Test-DecisionLogIds -Path $decisionLogTemplate -AllowPlaceholder

# 8. Project doc headings
$projectsDir = Join-Path $Root "Workspace/Projects"
Test-ProjectDocHeadings -ProjectRoot $projectsDir -Filename "project-memory-card.md" -Headings $projectMemoryHeadings
Test-ProjectDocHeadings -ProjectRoot $projectsDir -Filename "project-retrospective.md" -Headings $retrospectiveHeadings
Test-ProjectDocHeadings -ProjectRoot $projectsDir -Filename "knowledge-synthesis.md" -Headings $knowledgeHeadings
Test-ProjectDocHeadings -ProjectRoot $projectsDir -Filename "decision-log.md" -Headings $decisionLogHeadings
Test-ProjectDecisionLogIds -ProjectRoot $projectsDir

# 9. Cleanup checks
Test-TempFiles
# Dashboard retired - no longer checked
Test-LegacyFilenames -ProjectRoot $projectsDir
Test-LegacyPathReferences -ScanRoots @(
    (Join-Path $Root "Workspace/Projects"),
    (Join-Path $Root "Workspace/Knowledge")
)
Test-LegacyTextReferences

# 10. Knowledge coverage sync
Test-CoverageSync

# --- Report ---
# Ensure console can display UTF-8 (Chinese project names, heading names)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

if ($issues.Count -gt 0) {
    $hostObj = $Host
    if ($hostObj.UI -and $hostObj.UI.WriteErrorLine) {
        $hostObj.UI.WriteErrorLine("Packging OS validation failed ($($issues.Count) issues):")
        foreach ($issue in $issues) {
            $hostObj.UI.WriteErrorLine("- $issue")
        }
    } else {
        Write-Host "Packging OS validation failed ($($issues.Count) issues):" -ForegroundColor Red
        foreach ($issue in $issues) {
            Write-Host "- $issue" -ForegroundColor Red
        }
    }
    exit 1
}

Write-Host "Packging OS validation passed." -ForegroundColor Green
exit 0
