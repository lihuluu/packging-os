@echo off
REM init-project.cmd — Windows entry point for project initialization
REM Usage: .claude\skills\packging-os-maintainer\scripts\init-project.cmd "Project Name"
REM All arguments are forwarded to the PowerShell script.

powershell -ExecutionPolicy Bypass -File "%~dp0init-project.ps1" %*
exit /b %ERRORLEVEL%
