@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 开始训练人脸模型。
".venv\Scripts\python.exe" "face\python\数据训练.py"
pause