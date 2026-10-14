# -*- coding: utf-8 -*-
import cv2
import socket
import io
import os
import numpy as np
import time
from PIL import Image

try:
    import msvcrt
except ImportError:
    msvcrt = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "img")
os.makedirs(SAVE_DIR, exist_ok=True)

PERSON_ID = 1
ESP32_PORT = 8001

def existing_index():
    maximum = 0
    prefix = "user.%d." % PERSON_ID
    for filename in os.listdir(SAVE_DIR):
        if filename.startswith(prefix) and filename.lower().endswith(".jpg"):
            parts = filename.split(".")
            try:
                maximum = max(maximum, int(parts[2]))
            except (IndexError, ValueError):
                pass
    return maximum + 1


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


def save_frame(frame, index):
    filename = "user.%d.%d.jpg" % (PERSON_ID, index)
    path = os.path.join(SAVE_DIR, filename)
    try:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        Image.fromarray(rgb).save(path, quality=95)
        print("已保存：", filename)
        return True
    except Exception as exc:
        print("保存失败：", filename, exc)
        return False


ESP32_HOST = os.environ.get("FACE_DOOR_ESP32_HOST") or discover_esp32()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 0))
sock.settimeout(0.2)

index = existing_index()
frame = None
last_hello = 0.0
last_discovery = 0.0
last_packet = 0.0
auto_remaining = 20
last_auto = 0.0
auto_start_at = None
show_preview = True
frame_ready_announced = False

try:
    cv2.namedWindow("Capture_test", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Capture_test", 640, 480)
except Exception:
    show_preview = False

print("ESP32-CAM:", ESP32_HOST)
print("请在当前黑色窗口操作：")
print("  A = 自动连续保存20张")
print("  S = 保存当前一张")
print("  Q或Esc = 退出")

while True:
    now = time.time()

    if now - last_discovery > 5 and now - last_packet > 2:
        ESP32_HOST = discover_esp32()
        last_discovery = now

    if now - last_hello > 2:
        sock.sendto(b"hello", (ESP32_HOST, ESP32_PORT))
        last_hello = now

    try:
        data, addr = sock.recvfrom(100000)
        last_packet = now
        image = Image.open(io.BytesIO(data))
        frame = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        if not frame_ready_announced:
            print("已收到图像，3秒后自动保存20张，请缓慢左右转动头部")
            auto_start_at = time.time() + 3
            frame_ready_announced = True
    except socket.timeout:
        pass
    except Exception as exc:
        print("图像处理失败：", exc)

    key = -1
    if frame is not None and show_preview:
        try:
            cv2.imshow("Capture_test", frame)
            key = cv2.waitKey(1) & 0xFF
        except Exception:
            show_preview = False

    if msvcrt is not None and msvcrt.kbhit():
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):
            msvcrt.getwch()
        elif ch:
            key = ord(ch[0])

    if key in (ord("a"), ord("A")):
        auto_remaining = 20
        last_auto = 0
        print("开始自动保存，请缓慢左右转动头部...")

    if key in (ord("s"), ord("S")):
        if frame is None:
            print("还没有收到摄像头图像")
        elif save_frame(frame, index):
            index += 1

    if key in (ord("q"), ord("Q"), 27):
        break

    if auto_remaining > 0 and frame is not None and auto_start_at is not None and now >= auto_start_at and now - last_auto >= 0.5:
        if save_frame(frame, index):
            index += 1
            auto_remaining -= 1
            if auto_remaining == 0:
                print("自动保存完成，共20张。按 Q 退出。")
        last_auto = now

sock.close()
cv2.destroyAllWindows()
print("录入结束，共保存到序号：", index - 1)