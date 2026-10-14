import ast, json, re, subprocess, sys
from pathlib import Path
text=Path('face/esp32-cam/camera.py').read_text(encoding='utf-8')
def get(n): return ast.literal_eval(re.search(rf'^{n}\s*=\s*(.+)$',text,re.M).group(1))
ssid=get('WIFI_SSID'); pw=get('WIFI_PASSWORD')
code=f'''import network,time
w=network.WLAN(network.STA_IF)
w.active(False); time.sleep(1); w.active(True); time.sleep(1)
w.connect({json.dumps(ssid)}, {json.dumps(pw)})
start=time.time()
last=None
while time.time()-start<60:
    s=w.status()
    if s!=last:
        print('t=',round(time.time()-start,1),'status=',s,'connected=',w.isconnected())
        last=s
    if w.isconnected():
        break
    time.sleep(1)
print('final=',w.isconnected(),w.status(),w.ifconfig())
'''
r=subprocess.run([sys.executable,'-m','mpremote','connect','COM11','exec',code],cwd=Path.cwd())
raise SystemExit(r.returncode)
