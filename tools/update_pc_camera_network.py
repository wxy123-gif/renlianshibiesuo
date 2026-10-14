from pathlib import Path

# Update recognition program.
p = Path('face/python/ESP32-cam摄像头识别.py')
text = p.read_text(encoding='utf-8')
text = text.replace('import serial\n', 'import serial\nimport time\n')
text = text.replace('UDP_PORT = 9090\n', 'ESP32_HOST = os.environ.get("FACE_DOOR_ESP32_HOST", "192.168.88.101")\nESP32_PORT = 8000\n')
text = text.replace('sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\nsock.bind(("0.0.0.0", UDP_PORT))\nprint("正在监听 UDP 9090，等待 ESP32-CAM 图像...")', 'sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\nsock.bind(("0.0.0.0", 0))\nsock.settimeout(1)\nlast_hello = 0.0\nprint("等待 ESP32-CAM:", ESP32_HOST, ESP32_PORT)')
text = text.replace('while True:\n    data, addr = sock.recvfrom(100000)\n    try:', 'while True:\n    now = time.time()\n    if now - last_hello > 2:\n        sock.sendto(b"hello", (ESP32_HOST, ESP32_PORT))\n        last_hello = now\n    try:\n        data, addr = sock.recvfrom(100000)\n    except socket.timeout:\n        continue\n    try:')
p.write_text(text, encoding='utf-8')

# Update capture program.
p = Path('face/python/ESP32摄像头人脸录入.py')
text = p.read_text(encoding='utf-8')
text = text.replace('import numpy as np\n', 'import numpy as np\nimport time\n')
text = text.replace('UDP_PORT = 9091\n', 'ESP32_HOST = os.environ.get("FACE_DOOR_ESP32_HOST", "192.168.88.101")\nESP32_PORT = 8001\n')
text = text.replace('sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\nsock.bind(("0.0.0.0", UDP_PORT))\nprint("正在监听 UDP 9091，等待 ESP32-CAM 图像...")', 'sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\nsock.bind(("0.0.0.0", 0))\nsock.settimeout(1)\nlast_hello = 0.0\nprint("等待 ESP32-CAM:", ESP32_HOST, ESP32_PORT)')
text = text.replace('while True:\n    data, addr = sock.recvfrom(100000)\n    try:', 'while True:\n    now = time.time()\n    if now - last_hello > 2:\n        sock.sendto(b"hello", (ESP32_HOST, ESP32_PORT))\n        last_hello = now\n    try:\n        data, addr = sock.recvfrom(100000)\n    except socket.timeout:\n        continue\n    try:')
p.write_text(text, encoding='utf-8')
print('PC scripts updated')
