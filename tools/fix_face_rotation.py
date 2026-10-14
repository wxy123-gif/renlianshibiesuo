from pathlib import Path

# Rotate live capture frames to upright.
p=Path('face/python/ESP32摄像头人脸录入.py')
t=p.read_text(encoding='utf-8')
t=t.replace('frame = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)\n', 'frame = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)\n        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)\n')
p.write_text(t,encoding='utf-8')

# Rotate recognition frames to match training orientation.
p=Path('face/python/ESP32-cam摄像头识别.py')
t=p.read_text(encoding='utf-8')
t=t.replace('frame = np.asarray(image)\n        face_detect_demo(frame)', 'frame = np.asarray(image)\n        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)\n        face_detect_demo(frame)')
p.write_text(t,encoding='utf-8')

# Training: try four rotations and use the first one where a face is found.
p=Path('face/python/数据训练.py')
t=p.read_text(encoding='utf-8')
old='''        pil_img = Image.open(image_path).convert("L")
        img_numpy = np.array(pil_img, "uint8")
        faces = face_detector.detectMultiScale(img_numpy)
        if len(faces) == 0:
            print("未检测到人脸，跳过：", filename)
            continue
        for x, y, w, h in faces:
            ids.append(label_id)
            faces_samples.append(img_numpy[y:y + h, x:x + w])
'''
new='''        pil_img = Image.open(image_path).convert("L")
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
'''
if old not in t:
    raise SystemExit('training face block not found')
t=t.replace(old,new)
p.write_text(t,encoding='utf-8')
print('rotation fix applied')
