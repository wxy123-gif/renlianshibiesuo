import ast, json, re, subprocess, sys
from pathlib import Path
text=Path('face/esp32-cam/camera.py').read_text(encoding='utf-8')
def get(n): return ast.literal_eval(re.search(rf'^{n}\s*=\s*(.+)$',text,re.M).group(1))
ssid=get('WIFI_SSID'); pw=get('WIFI_PASSWORD')
code=f'''import network,time
w=network.WLAN(network.STA_IF)
w.active(False); time.sleep(1); w.active(True); time.sleep(1)
try:
    w.config(txpower=8.5)
    print('txpower=',w.config('txpower'))
except Exception as e:
    print('txpower_set_failed=',e)
w.connect({json.dumps(ssid)}, {json.dumps(pw)})
deadline=time.time()+45
while not w.isconnected() and time.time()<deadline:
    time.sleep(1)
print('connected=',w.isconnected())
print('status=',w.status())
print('ip=',w.ifconfig()[0])
'''
r=subprocess.run([sys.executable,'-m','mpremote','connect','COM11','exec',code],cwd=Path.cwd())
raise SystemExit(r.returncode)
