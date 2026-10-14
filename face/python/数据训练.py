# -*- coding: utf-8 -*-
import os
import shutil
import cv2
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "img")
TRAINER_DIR = os.path.join(BASE_DIR, "trainer")
TRAINER_FILE = os.path.join(TRAINER_DIR, "trainer.yml")
os.makedirs(TRAINER_DIR, exist_ok=True)

# OpenCV FileStorage cannot reliably open paths containing Chinese characters.
CACHE_DIR = r"C:\Users\Public\FaceDoor"
os.makedirs(CACHE_DIR, exist_ok=True)
CLASSIFIER_FILE = os.path.join(CACHE_DIR, "haarcascade_frontalface_alt2.xml")
TRAINER_CACHE_FILE = os.path.join(CACHE_DIR, "trainer.yml")
if not os.path.exists(CLASSIFIER_FILE):
    shutil.copyfile(os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_alt2.xml"), CLASSIFIER_FILE)

face_detector = cv2.CascadeClassifier(CLASSIFIER_FILE)
if face_detector.empty():
    raise SystemExit("无法加载 OpenCV 人脸检测器")

def get_image_and_labels(path):
    if not os.path.isdir(path):
        raise SystemExit("图片目录不存在：" + path)
    files = sorted(
        f for f in os.listdir(path)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    )
    if not files:
        raise SystemExit("img 目录没有图片，请先运行人脸录入程序")

    faces_samples = []
    ids = []
    for filename in files:
        image_path = os.path.join(path, filename)
        parts = filename.split(".")
        try:
            label_id = int(parts[1]) if len(parts) >= 3 and parts[0] == "user" else int(parts[0])
        except ValueError:
            print("跳过无法识别 ID 的文件：", filename)
            continue

        pil_img = Image.open(image_path).convert("L")
        img_numpy = np.array(pil_img, "uint8")
        faces = []
        rotated = img_numpy
        rotations = (
            None,
            cv2.ROTATE_90_CLOCKWISE,
            cv2.ROTATE_90_COUNTERCLOCKWISE,
            cv2.ROTATE_180,
        )
        for rotation in rotations:
            candidate = img_numpy if rotation is None else cv2.rotate(img_numpy, rotation)
            found = face_detector.detectMultiScale(candidate)
            if len(found) > 0:
                rotated = candidate
                faces = found
                break
        if len(faces) == 0:
            print("未检测到人脸，跳过：", filename)
            continue
        for x, y, w, h in faces:
            ids.append(label_id)
            faces_samples.append(rotated[y:y + h, x:x + w])

    if not faces_samples:
        raise SystemExit("没有检测到可训练的人脸，请重新录入清晰照片")
    return faces_samples, ids

faces, ids = get_image_and_labels(IMAGE_DIR)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(ids))
recognizer.write(TRAINER_CACHE_FILE)
shutil.copyfile(TRAINER_CACHE_FILE, TRAINER_FILE)
print("训练完成，共使用 %d 张人脸样本" % len(faces))
print("模型已保存：" + TRAINER_FILE)