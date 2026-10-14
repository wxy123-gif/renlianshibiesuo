import socket,io,os,time,cv2,numpy as np
from PIL import Image
cache=r'C:\Users\Public\FaceDoor'
clf=cv2.CascadeClassifier(os.path.join(cache,'haarcascade_frontalface_alt2.xml'))
rec=cv2.face.LBPHFaceRecognizer_create(); rec.read(os.path.join(cache,'trainer.yml'))
# discover
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.bind(('0.0.0.0',0)); s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1); s.settimeout(0.5)
host=None
for _ in range(8):
    s.sendto(b'discover',('255.255.255.255',8888))
    try: host=s.recvfrom(64)[0].decode().strip(); break
    except socket.timeout: pass
s.close(); print('host=',host)
if not host: raise SystemExit('no host')
# receive 8000
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.bind(('0.0.0.0',0)); s.settimeout(1)
for _ in range(20):
    s.sendto(b'hello',(host,8000))
    try: data,addr=s.recvfrom(100000); break
    except socket.timeout: data=None
s.close()
if not data: raise SystemExit('no image')
frame=cv2.cvtColor(np.asarray(Image.open(io.BytesIO(data))),cv2.COLOR_RGB2BGR)
frame=cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
faces=clf.detectMultiScale(gray,1.1,5,cv2.CASCADE_SCALE_IMAGE,(100,100),(300,300))
print('faces=',len(faces))
for x,y,w,h in faces:
    label,conf=rec.predict(gray[y:y+h,x:x+w]); print('label=',label,'confidence=',round(float(conf),2))
