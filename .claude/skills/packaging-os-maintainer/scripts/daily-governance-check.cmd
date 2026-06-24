@echo off
setlocal EnableExtensions

set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%..\..\..\.."
for %%I in ("%ROOT_DIR%") do set "ROOT_DIR=%%~fI"
set "FAILED=0"

echo Packaging OS - daily governance check
echo Repository: %ROOT_DIR%
echo.

echo [1/3] Governance validation
call "%SCRIPT_DIR%validate-packaging-os.cmd"
if errorlevel 1 set "FAILED=1"
echo.

echo [2/3] Project temp cleanup dry-run
call "%SCRIPT_DIR%..\..\project-memory-manager\scripts\cleanup-project-temp-files.cmd"
if errorlevel 1 set "FAILED=1"
echo.

echo [3/3] Project memory drift check
python --version >nul 2>nul
if not errorlevel 1 (
  python "%SCRIPT_DIR%..\..\project-memory-manager\scripts\check-memory-drift.py" --root "%ROOT_DIR%" --all
  if errorlevel 1 set "FAILED=1"
) else (
  py -3 --version >nul 2>nul
  if not errorlevel 1 (
    py -3 "%SCRIPT_DIR%..\..\project-memory-manager\scripts\check-memory-drift.py" --root "%ROOT_DIR%" --all
    if errorlevel 1 set "FAILED=1"
  ) else (
    echo [skip] Python was not found, so project memory drift check was skipped.
  )
)

echo.
if "%FAILED%"=="1" (
  echo Daily governance check completed with issues.
  exit /b 1
)

echo Daily governance check passed.
exit /b 0
