import socket,time
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.bind(('0.0.0.0',0)); s.settimeout(1)
got=False
for i in range(15):
    s.sendto(b'hello',('192.168.88.101',8000))
    try:
        data,addr=s.recvfrom(100000); print('port8000 received_bytes',len(data),'sender',addr); got=True; break
    except socket.timeout: pass
print('success=',got)
s.close()
