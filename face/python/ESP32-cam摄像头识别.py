# -*- coding: utf-8 -*-
import cv2
import socket
import io
import os
import shutil
import numpy as np
from PIL import Image
import serial
import serial.tools.list_ports
import time


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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINER_FILE = os.path.join(BASE_DIR, "trainer", "trainer.yml")
IMAGE_DIR = os.path.join(BASE_DIR, "img")
CACHE_DIR = r"C:\Users\Public\FaceDoor"
os.makedirs(CACHE_DIR, exist_ok=True)
CLASSIFIER_FILE = os.path.join(CACHE_DIR, "haarcascade_frontalface_alt2.xml")
TRAINER_CACHE_FILE = os.path.join(CACHE_DIR, "trainer.yml")
if not os.path.exists(CLASSIFIER_FILE):
    shutil.copyfile(os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_alt2.xml"), CLASSIFIER_FILE)
ESP32_HOST = os.environ.get("FACE_DOOR_ESP32_HOST") or discover_esp32()
last_discovery = 0.0
last_packet = 0.0
ESP32_PORT = 8000
SERIAL_BAUD = 9600

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
UNLOCK_COMMAND = bytes.fromhex("ffabcdfe")

if not os.path.exists(TRAINER_FILE):
    raise SystemExit("没有找到训练模型：" + TRAINER_FILE + "\n请先运行 数据训练.py")

shutil.copyfile(TRAINER_FILE, TRAINER_CACHE_FILE)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(TRAINER_CACHE_FILE)

face_detector = cv2.CascadeClassifier(CLASSIFIER_FILE)
if face_detector.empty():
    raise SystemExit("无法加载 OpenCV 人脸检测器")

name_map = {}
if os.path.isdir(IMAGE_DIR):
    for filename in os.listdir(IMAGE_DIR):
        parts = filename.split(".")
        if len(parts) >= 3 and parts[0] == "user":
            try:
                name_map[int(parts[1])] = parts[1]
            except ValueError:
                pass

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 0))
sock.settimeout(1)
last_hello = 0.0
print("等待 ESP32-CAM:", ESP32_HOST, ESP32_PORT)

def send_unlock_command():
    try:
        with serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1) as uart:
            uart.write(UNLOCK_COMMAND)
            print("已向 STM32 发送开门命令")
    except Exception as exc:
        print("串口发送失败：", exc, "当前串口：", SERIAL_PORT)

def face_detect_demo(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(
        gray, 1.1, 5, cv2.CASCADE_SCALE_IMAGE, (100, 100), (300, 300)
    )

    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.circle(img, (x + w // 2, y + h // 2), w // 2, (0, 255, 0), 1)
        ids, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        if confidence > 50:
            text = "unknown"
            color = (0, 0, 255)
        else:
            text = name_map.get(ids, str(ids))
            color = (0, 255, 0)
            send_unlock_command()
        cv2.putText(img, text, (x + 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

    cv2.imshow("result", img)

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
    except socket.timeout:
        continue
    try:
        image = Image.open(io.BytesIO(data))
        frame = np.asarray(image)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        face_detect_demo(frame)
    except Exception as exc:
        print("图像处理失败：", exc)

    if cv2.waitKey(10) == 27:
        break

sock.close()
cv2.destroyAllWindows()