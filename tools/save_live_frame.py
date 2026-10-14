import socket,io,time,cv2,numpy as np
from PIL import Image
# discover
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.bind(('0.0.0.0',0)); s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1); s.settimeout(0.5)
host=None
for _ in range(8):
    s.sendto(b'discover',('255.255.255.255',8888))
    try: host=s.recvfrom(64)[0].decode().strip(); break
    except socket.timeout: pass
s.close()
# receive
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.bind(('0.0.0.0',0)); s.settimeout(1); data=None
for _ in range(20):
    s.sendto(b'hello',(host,8000))
    try: data,addr=s.recvfrom(100000); break
    except socket.timeout: pass
s.close()
if data:
    raw=Image.open(io.BytesIO(data)); raw.save('_eda_work/live_raw.jpg')
    frame=cv2.cvtColor(np.asarray(raw),cv2.COLOR_RGB2BGR); frame=cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
    Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)).save('_eda_work/live_rotated.jpg')
    print('saved',len(data))
else: print('no image')
