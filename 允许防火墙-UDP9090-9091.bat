@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在请求管理员权限，请在 UAC 窗口点击“是”...
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Start-Process powershell.exe -Verb RunAs -Wait -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File','%~dp0tools\allow_face_door_firewall.ps1')"
echo.
echo 执行结果：
if exist "%~dp0tools\firewall_result.txt" (
    type "%~dp0tools\firewall_result.txt"
) else (
    echo 没有生成结果文件，可能取消了 UAC 或执行失败。
)
pause