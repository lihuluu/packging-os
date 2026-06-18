@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%..\..\..\.."

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8; & '%SCRIPT_DIR%validate-packging-os.ps1' -Root '%ROOT_DIR%'; exit $LASTEXITCODE"
exit /b %ERRORLEVEL%
