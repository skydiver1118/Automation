@echo off
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "scripts\setup_gmail_alerts.ps1" -SendTest -PersistUserEnv
pause
