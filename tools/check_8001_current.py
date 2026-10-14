import socket,time
host='192.168.88.102'
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.bind(('0.0.0.0',0)); s.settimeout(1)
for i in range(12):
    s.sendto(b'hello',(host,8001))
    try:
        data,addr=s.recvfrom(100000); print('received_bytes',len(data),addr); break
    except socket.timeout: pass
else: print('received=False')
s.close()
