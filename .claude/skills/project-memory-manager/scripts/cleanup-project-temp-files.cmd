@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%..\..\..\.."
set "ARGS=%*"

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8; & '%SCRIPT_DIR%cleanup-project-temp-files.ps1' -Root '%ROOT_DIR%' %ARGS%; exit $LASTEXITCODE"
exit /b %ERRORLEVEL%
