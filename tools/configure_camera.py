import re
from pathlib import Path
p=Path('face/esp32-cam/camera.py')
text=p.read_text(encoding='utf-8')
text=re.sub(r'^WIFI_SSID\s*=.*$', 'WIFI_SSID = "YOUR_WIFI_SSID"', text, flags=re.M)
text=re.sub(r'^WIFI_PASSWORD\s*=.*$', 'WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"', text, flags=re.M)
text=re.sub(r'^SERVER_IP\s*=.*$', 'SERVER_IP = "192.168.88.100"', text, flags=re.M)
text=re.sub(r'^RECOGNITION_PORT\s*=.*$', 'RECOGNITION_PORT = 9090', text, flags=re.M)
text=re.sub(r'^CAPTURE_PORT\s*=.*$', 'CAPTURE_PORT = 9091', text, flags=re.M)
p.write_text(text, encoding='utf-8')
print('camera.py configured')
