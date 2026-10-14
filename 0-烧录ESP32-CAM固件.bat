@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PORT=COM11
echo.
echo 烧录前确认：
echo 1. IO0 已接 GND
echo 2. ESP32-CAM 已接 5V 电源
echo 3. 已关闭串口监视器、Arduino IDE、Thonny
echo.
set /p USERPORT=请输入串口号，直接回车使用 COM11：
if not "%USERPORT%"=="" set PORT=%USERPORT%
echo 使用串口 %PORT%
echo.
echo 正在擦除 ESP32-CAM Flash...
".venv\Scripts\python.exe" -m esptool --chip esp32 --port %PORT% erase_flash
if errorlevel 1 goto fail
echo.
echo 正在烧录 MicroPython 摄像头固件...
".venv\Scripts\python.exe" -m esptool --chip esp32 --port %PORT% --baud 460800 write_flash -z 0x1000 "face\esp32-cam\micropython_v1.21.0_camera_no_ble.bin"
if errorlevel 1 goto fail
echo.
echo 固件烧录完成。请断开 IO0 和 GND，然后拔插一次 ESP32-CAM 电源。
pause
exit /b 0
:fail
echo.
echo 烧录失败。请检查串口号、接线和串口占用。
pause
exit /b 1