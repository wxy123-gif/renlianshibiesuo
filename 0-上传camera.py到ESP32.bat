@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PORT=COM11
echo.
echo 上传前确认：
echo 1. IO0 已断开 GND，ESP32-CAM 已重新上电
echo 2. 已关闭串口监视器
echo 3. camera.py 中的 WiFi 名称和密码已经修改
echo.
set /p USERPORT=请输入串口号，直接回车使用 COM11：
if not "%USERPORT%"=="" set PORT=%USERPORT%
echo 使用串口 %PORT%
echo.
echo 正在上传 camera.py 为 main.py...
".venv\Scripts\python.exe" -m mpremote connect %PORT% fs cp "face\esp32-cam\camera.py" :main.py
if errorlevel 1 goto fail
echo.
echo 上传完成。ESP32-CAM 重新上电后会自动运行 main.py。
pause
exit /b 0
:fail
echo.
echo 上传失败。请检查串口号和 ESP32-CAM 是否已进入运行模式。
pause
exit /b 1