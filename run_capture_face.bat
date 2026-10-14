@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo 人脸录入窗口即将启动。
echo 在当前黑色窗口按 A 自动保存20张照片。
echo 按 Q 或 Esc 结束。
echo.
".venv\Scripts\python.exe" "face\python\capture_face.py"
echo.
pause