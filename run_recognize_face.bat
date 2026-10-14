@echo off
chcp 65001 >nul
cd /d "%~dp0"
".venv\Scripts\python.exe" "face\python\recognize_face.py"
pause