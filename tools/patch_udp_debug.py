from pathlib import Path
p=Path('face/esp32-cam/camera.py')
t=p.read_text(encoding='utf-8')
needle='            if data == b"hello":'
replacement='            if data:\n                print("UDP收到", port, repr(data), addr)\n            if data == b"hello":'
if 'UDP收到' not in t:
    t=t.replace(needle,replacement)
p.write_text(t,encoding='utf-8')
print('patched=', 'UDP收到' in t)
