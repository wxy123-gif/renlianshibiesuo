@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 启动人脸录入，按 s 保存图片，按 Esc 退出。
".venv\Scripts\python.exe" "face\python\ESP32摄像头人脸录入.py"
pause