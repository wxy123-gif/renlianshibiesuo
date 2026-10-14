from pathlib import Path
p=Path('face/python/ESP32-cam摄像头识别.py')
text=p.read_text(encoding='utf-8')
text=text.replace('import serial\nimport time\n','import serial\nimport serial.tools.list_ports\nimport time\n')
old='SERIAL_PORT = os.environ.get("FACE_DOOR_SERIAL_PORT", "COM7")\nSERIAL_BAUD = 9600\n'
new='''SERIAL_BAUD = 9600

def choose_serial_port():
    configured = os.environ.get("FACE_DOOR_SERIAL_PORT")
    if configured:
        return configured
    candidates = []
    for port in serial.tools.list_ports.comports():
        text = ((port.description or "") + " " + (port.hwid or "")).lower()
        if port.device == "COM11" or "bluetooth" in text or "bth" in text:
            continue
        candidates.append(port.device)
    return candidates[0] if len(candidates) == 1 else "COM7"

SERIAL_PORT = choose_serial_port()
'''
if old not in text:
    raise SystemExit('serial config block not found')
text=text.replace(old,new)
p.write_text(text,encoding='utf-8')
print('recognition serial auto-detect updated')
