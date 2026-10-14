from pathlib import Path
p=Path('face/esp32-cam/camera.py')
t=p.read_text(encoding='utf-8')
t=t.replace('            if data:\n                print("UDP收到", port, repr(data), addr)\n','')
p.write_text(t,encoding='utf-8')
print('debug_log_removed=', 'UDP收到' not in t)
