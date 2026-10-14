import ast
import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
text = (root / 'face' / 'esp32-cam' / 'camera.py').read_text(encoding='utf-8')
def get(name):
    m = re.search(rf'^{name}\s*=\s*(.+)$', text, flags=re.M)
    if not m:
        raise SystemExit(f'{name} not found')
    return ast.literal_eval(m.group(1))
ssid = get('WIFI_SSID')
password = get('WIFI_PASSWORD')
code = f'''import network,time
w=network.WLAN(network.STA_IF)
w.active(False)
time.sleep(1)
w.active(True)
time.sleep(1)
print("before=", w.status())
w.connect({json.dumps(ssid)}, {json.dumps(password)})
deadline=time.time()+30
while not w.isconnected() and time.time()<deadline:
    time.sleep(0.5)
print("connected=", w.isconnected())
print("status=", w.status())
print("ip=", w.ifconfig()[0])
'''
result = subprocess.run([sys.executable, '-m', 'mpremote', 'connect', 'COM11', 'exec', code], cwd=root)
raise SystemExit(result.returncode)
