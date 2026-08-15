@echo off
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "scripts\check_stock_alert_setup.ps1"
pause
