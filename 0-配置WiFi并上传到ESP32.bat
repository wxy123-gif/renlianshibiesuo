@echo off
chcp 65001 >nul
cd /d "%~dp0"
".venv\Scripts\python.exe" "tools\configure_and_upload_esp32.py"
pause