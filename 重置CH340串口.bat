@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在请求管理员权限，请在 UAC 窗口点击“是”...
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Start-Process powershell.exe -Verb RunAs -Wait -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File','%~dp0tools\reset_ch340.ps1')"
echo.
pause