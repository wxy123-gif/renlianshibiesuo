# -*- coding: utf-8 -*-
import getpass
import re
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
camera_file = root / "face" / "esp32-cam" / "camera.py"

print("配置 ESP32-CAM WiFi")
ssid = input("请输入 2.4GHz WiFi 名称：").strip()
if not ssid:
    raise SystemExit("WiFi 名称不能为空")
password = getpass.getpass("请输入 WiFi 密码（输入时不会显示）：")
port = input("请输入串口号，直接回车使用 COM11：").strip() or "COM11"
server_ip = input("请输入电脑 IP，直接回车使用 192.168.88.100：").strip() or "192.168.88.100"

text = camera_file.read_text(encoding="utf-8")
text = re.sub(r'^WIFI_SSID\s*=\s*".*"$', 'WIFI_SSID = ' + repr(ssid), text, flags=re.M)
text = re.sub(r'^WIFI_PASSWORD\s*=\s*".*"$', 'WIFI_PASSWORD = ' + repr(password), text, flags=re.M)
text = re.sub(r'^SERVER_IP\s*=\s*".*"$', 'SERVER_IP = ' + repr(server_ip), text, flags=re.M)
camera_file.write_text(text, encoding="utf-8")

print("\n正在上传到 ESP32-CAM...")
result = subprocess.run(
    [sys.executable, "-m", "mpremote", "connect", port, "fs", "cp",
     str(camera_file), ":main.py"],
    cwd=root,
)
if result.returncode != 0:
    raise SystemExit("上传失败，请检查 COM 口和接线")
print("\n上传成功。ESP32-CAM 重新上电后会自动连接 WiFi 并发送图像。")