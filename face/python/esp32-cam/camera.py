import socket
import network
import camera
import time

# 2.4GHz WiFi
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# ESP32-CAM 等待电脑连接的服务端口
RECOGNITION_PORT = 8000
CAPTURE_PORT = 8001
DISCOVERY_PORT = 8888

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print("connecting to network...")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    deadline = time.time() + 20
    while not wlan.isconnected() and time.time() < deadline:
        time.sleep(0.5)

if not wlan.isconnected():
    print("WiFi connection failed:", WIFI_SSID)
    raise SystemExit

print("WiFi OK:", wlan.ifconfig())

try:
    camera.init(0, format=camera.JPEG, framesize=camera.FRAME_QVGA,
                xclk_freq=camera.XCLK_10MHz)
except Exception:
    camera.deinit()
    camera.init(0, format=camera.JPEG, framesize=camera.FRAME_QVGA,
                xclk_freq=camera.XCLK_10MHz)

camera.flip(0)
camera.mirror(1)
camera.speffect(camera.EFFECT_NONE)
camera.whitebalance(camera.WB_NONE)
camera.saturation(0)
camera.brightness(0)
camera.contrast(0)
camera.quality(10)

recognition_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recognition_socket.bind(("0.0.0.0", RECOGNITION_PORT))
recognition_socket.setblocking(False)

capture_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
capture_socket.bind(("0.0.0.0", CAPTURE_PORT))
capture_socket.setblocking(False)

discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
discovery_socket.bind(("0.0.0.0", DISCOVERY_PORT))
discovery_socket.setblocking(False)

clients = {RECOGNITION_PORT: None, CAPTURE_PORT: None}
sockets = {RECOGNITION_PORT: recognition_socket, CAPTURE_PORT: capture_socket}
print("等待电脑连接端口:", RECOGNITION_PORT, CAPTURE_PORT)

while True:
    try:
        message, addr = discovery_socket.recvfrom(64)
        if message == b"discover":
            discovery_socket.sendto(wlan.ifconfig()[0].encode(), addr)
    except OSError:
        pass

    for port, sock in sockets.items():
        try:
            data, addr = sock.recvfrom(64)
            if data == b"hello":
                clients[port] = addr
                print("电脑已连接端口", port, addr)
        except OSError:
            pass

    if clients[RECOGNITION_PORT] or clients[CAPTURE_PORT]:
        buf = camera.capture()
        if isinstance(buf, (bytes, bytearray)):
            for port, addr in clients.items():
                if addr:
                    sockets[port].sendto(buf, addr)
    time.sleep(0.1)