import os, cv2, numpy as np
from PIL import Image
cache=r'C:\Users\Public\FaceDoor'
clf=cv2.CascadeClassifier(os.path.join(cache,'haarcascade_frontalface_alt2.xml'))
rec=cv2.face.LBPHFaceRecognizer_create(); rec.read(os.path.join(cache,'trainer.yml'))
img=np.array(Image.open('face/python/img/user.1.1.jpg').convert('L'))
for name,rot in [('none',None),('cw',cv2.ROTATE_90_CLOCKWISE),('ccw',cv2.ROTATE_90_COUNTERCLOCKWISE),('180',cv2.ROTATE_180)]:
    x=img if rot is None else cv2.rotate(img,rot)
    faces=clf.detectMultiScale(x)
    if len(faces):
        for a,b,w,h in faces:
            label,conf=rec.predict(x[b:b+h,a:a+w]); print('rotation',name,'label',label,'confidence',round(float(conf),2)); raise SystemExit(0)
print('no face detected')
