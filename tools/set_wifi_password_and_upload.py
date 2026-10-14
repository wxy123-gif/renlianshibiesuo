# -*- coding: utf-8 -*-
import os
import re
import subprocess
import sys
from pathlib import Path

password = os.environ.get('FACE_DOOR_WIFI_PASSWORD')
if not password:
    raise SystemExit('missing FACE_DOOR_WIFI_PASSWORD')
root = Path(__file__).resolve().parents[1]
camera_file = root / 'face' / 'esp32-cam' / 'camera.py'
text = camera_file.read_text(encoding='utf-8')
text = re.sub(r'^WIFI_PASSWORD\s*=\s*.*$', 'WIFI_PASSWORD = ' + repr(password), text, flags=re.M)
camera_file.write_text(text, encoding='utf-8')
result = subprocess.run(
    [sys.executable, '-m', 'mpremote', 'connect', 'COM11', 'fs', 'cp',
     str(camera_file), ':main.py'],
    cwd=root,
)
if result.returncode:
    raise SystemExit(result.returncode)
print('password_updated=True')
print('uploaded=True')