from pathlib import Path

# Training script
p=Path('face/python/数据训练.py')
t=p.read_text(encoding='utf-8')
t=t.replace('import os\nimport cv2\n','import os\nimport shutil\nimport cv2\n')
t=t.replace('TRAINER_FILE = os.path.join(TRAINER_DIR, "trainer.yml")\nos.makedirs(TRAINER_DIR, exist_ok=True)\n\nface_detector = cv2.CascadeClassifier(\n    os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_alt2.xml")\n)','TRAINER_FILE = os.path.join(TRAINER_DIR, "trainer.yml")\nos.makedirs(TRAINER_DIR, exist_ok=True)\n\n# OpenCV FileStorage cannot reliably open paths containing Chinese characters.\nCACHE_DIR = r"C:\\Users\\Public\\FaceDoor"\nos.makedirs(CACHE_DIR, exist_ok=True)\nCLASSIFIER_FILE = os.path.join(CACHE_DIR, "haarcascade_frontalface_alt2.xml")\nTRAINER_CACHE_FILE = os.path.join(CACHE_DIR, "trainer.yml")\nif not os.path.exists(CLASSIFIER_FILE):\n    shutil.copyfile(os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_alt2.xml"), CLASSIFIER_FILE)\n\nface_detector = cv2.CascadeClassifier(CLASSIFIER_FILE)')
t=t.replace('recognizer.write(TRAINER_FILE)\nprint("训练完成，共使用 %d 张人脸样本" % len(faces))\nprint("模型已保存：" + TRAINER_FILE)','recognizer.write(TRAINER_CACHE_FILE)\nshutil.copyfile(TRAINER_CACHE_FILE, TRAINER_FILE)\nprint("训练完成，共使用 %d 张人脸样本" % len(faces))\nprint("模型已保存：" + TRAINER_FILE)')
p.write_text(t,encoding='utf-8')

# Recognition script
p=Path('face/python/ESP32-cam摄像头识别.py')
t=p.read_text(encoding='utf-8')
t=t.replace('import os\nimport numpy as np\n','import os\nimport shutil\nimport numpy as np\n')
t=t.replace('''BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINER_FILE = os.path.join(BASE_DIR, "trainer", "trainer.yml")
IMAGE_DIR = os.path.join(BASE_DIR, "img")
''','''BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINER_FILE = os.path.join(BASE_DIR, "trainer", "trainer.yml")
IMAGE_DIR = os.path.join(BASE_DIR, "img")
CACHE_DIR = r"C:\\Users\\Public\\FaceDoor"
os.makedirs(CACHE_DIR, exist_ok=True)
CLASSIFIER_FILE = os.path.join(CACHE_DIR, "haarcascade_frontalface_alt2.xml")
TRAINER_CACHE_FILE = os.path.join(CACHE_DIR, "trainer.yml")
if not os.path.exists(CLASSIFIER_FILE):
    shutil.copyfile(os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_alt2.xml"), CLASSIFIER_FILE)
''')
t=t.replace('''if not os.path.exists(TRAINER_FILE):
    raise SystemExit("没有找到训练模型：" + TRAINER_FILE + "\\n请先运行 数据训练.py")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(TRAINER_FILE)

face_detector = cv2.CascadeClassifier(
    os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_alt2.xml")
)
''','''if not os.path.exists(TRAINER_FILE):
    raise SystemExit("没有找到训练模型：" + TRAINER_FILE + "\\n请先运行 数据训练.py")

shutil.copyfile(TRAINER_FILE, TRAINER_CACHE_FILE)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(TRAINER_CACHE_FILE)

face_detector = cv2.CascadeClassifier(CLASSIFIER_FILE)
''')
p.write_text(t,encoding='utf-8')
print('unicode cache support added')
