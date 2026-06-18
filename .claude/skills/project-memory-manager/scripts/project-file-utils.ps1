function Get-ProjectTempPath {
    param([string]$Path)

    return "{0}.tmp.{1}.{2}" -f $Path, $PID, ([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds())
}

function Remove-ProjectTempFiles {
    param([string]$TargetPath)

    $directory = Split-Path -Parent $TargetPath
    $fileName = Split-Path -Leaf $TargetPath

    if (-not (Test-Path $directory)) {
        return
    }

    Get-ChildItem -Path $directory -File -Filter "$fileName.tmp.*" -ErrorAction SilentlyContinue |
        Remove-Item -Force -ErrorAction SilentlyContinue
}

function Write-ProjectFileAtomic {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [AllowEmptyCollection()]
        [AllowEmptyString()]
        [string[]]$Lines
    )

    $directory = Split-Path -Parent $Path
    if (-not (Test-Path $directory)) {
        New-Item -ItemType Directory -Path $directory | Out-Null
    }

    $tempPath = Get-ProjectTempPath -Path $Path

    try {
        Set-Content -Path $tempPath -Value ($Lines -join "`r`n") -Encoding UTF8
        Move-Item -Path $tempPath -Destination $Path -Force
        Remove-ProjectTempFiles -TargetPath $Path
    } catch {
        Write-Error ("Failed to write project file: {0}" -f $Path)
        if (Test-Path $tempPath) {
            Write-Error ("Temporary file preserved: {0}" -f $tempPath)
        }
        throw
    }
}
