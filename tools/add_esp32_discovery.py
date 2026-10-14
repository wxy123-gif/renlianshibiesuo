from pathlib import Path

# Patch ESP32 discovery responder.
p=Path('face/esp32-cam/camera.py')
t=p.read_text(encoding='utf-8')
if 'DISCOVERY_PORT' not in t:
    t=t.replace('CAPTURE_PORT = 8001\n','CAPTURE_PORT = 8001\nDISCOVERY_PORT = 8888\n')
    t=t.replace('clients = {RECOGNITION_PORT: None, CAPTURE_PORT: None}\n','discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\ndiscovery_socket.bind(("0.0.0.0", DISCOVERY_PORT))\ndiscovery_socket.setblocking(False)\n\nclients = {RECOGNITION_PORT: None, CAPTURE_PORT: None}\n')
    t=t.replace('while True:\n    for port, sock in sockets.items():','while True:\n    try:\n        message, addr = discovery_socket.recvfrom(64)\n        if message == b"discover":\n            discovery_socket.sendto(wlan.ifconfig()[0].encode(), addr)\n    except OSError:\n        pass\n\n    for port, sock in sockets.items():')
p.write_text(t,encoding='utf-8')

# Patch PC discovery helper.
helper='''
def discover_esp32():
    configured = os.environ.get("FACE_DOOR_ESP32_HOST")
    if configured:
        return configured
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 0))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(0.5)
    try:
        for _ in range(6):
            sock.sendto(b"discover", ("255.255.255.255", 8888))
            try:
                data, addr = sock.recvfrom(64)
                return data.decode().strip()
            except socket.timeout:
                pass
    finally:
        sock.close()
    return "192.168.88.101"

'''
for rel in ['face/python/ESP32-cam摄像头识别.py','face/python/ESP32摄像头人脸录入.py']:
    p=Path(rel); t=p.read_text(encoding='utf-8')
    if 'def discover_esp32' not in t:
        t=t.replace('BASE_DIR = os.path.dirname(os.path.abspath(__file__))\n', helper+'BASE_DIR = os.path.dirname(os.path.abspath(__file__))\n')
        marker='ESP32_HOST = os.environ.get("FACE_DOOR_ESP32_HOST", "192.168.88.101")\n'
        if marker in t:
            t=t.replace(marker,'ESP32_HOST = discover_esp32()\n')
        else:
            # recognition script has an extra serial block between BASE_DIR and host
            t=t.replace('ESP32_HOST = os.environ.get("FACE_DOOR_ESP32_HOST", "192.168.88.101")\n','ESP32_HOST = discover_esp32()\n')
    p.write_text(t,encoding='utf-8')
print('discovery support added')
