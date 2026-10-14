@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 启动人脸识别。电脑 IP 必须为 192.168.88.100。
".venv\Scripts\python.exe" "face\python\ESP32-cam摄像头识别.py"
pause