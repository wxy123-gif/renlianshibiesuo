from pathlib import Path
for rel in ['face/python/ESP32摄像头人脸录入.py','face/python/ESP32-cam摄像头识别.py']:
    p=Path(rel); t=p.read_text(encoding='utf-8')
    t=t.replace('ESP32_HOST = discover_esp32()\n','ESP32_HOST = os.environ.get("FACE_DOOR_ESP32_HOST") or discover_esp32()\nlast_discovery = 0.0\nlast_packet = 0.0\n')
    t=t.replace('while True:\n    now = time.time()\n    if now - last_hello > 2:\n        sock.sendto(b"hello", (ESP32_HOST, ESP32_PORT))\n        last_hello = now',
                'while True:\n    now = time.time()\n    if now - last_discovery > 5 and now - last_packet > 2:\n        ESP32_HOST = discover_esp32()\n        last_discovery = now\n    if now - last_hello > 2:\n        sock.sendto(b"hello", (ESP32_HOST, ESP32_PORT))\n        last_hello = now')
    t=t.replace('        data, addr = sock.recvfrom(100000)\n    except socket.timeout:\n        continue', '        data, addr = sock.recvfrom(100000)\n        last_packet = now\n    except socket.timeout:\n        continue')
    p.write_text(t,encoding='utf-8')
print('dynamic rediscovery added')
