@echo off
setlocal

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0check-memory-drift.ps1" %*
exit /b %ERRORLEVEL%
