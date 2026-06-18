@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%..\..\..\.."

if "%~1"=="" (
  echo Usage: sync-project.cmd --project ^<project-name^>
  exit /b 1
)

where python >nul 2>&1
if %errorlevel%==0 (
  python "%SCRIPT_DIR%sync-project.py" --root "%ROOT_DIR%" %*
  exit /b %errorlevel%
)

where python3 >nul 2>&1
if %errorlevel%==0 (
  python3 "%SCRIPT_DIR%sync-project.py" --root "%ROOT_DIR%" %*
  exit /b %errorlevel%
)

echo Error: sync-project requires Python (python or python3) on PATH. >&2
exit /b 1
