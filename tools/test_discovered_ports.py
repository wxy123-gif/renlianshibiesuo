import socket,time

def discover():
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.bind(('0.0.0.0',0)); s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1); s.settimeout(0.5)
    try:
        for _ in range(6):
            s.sendto(b'discover',('255.255.255.255',8888))
            try: return s.recvfrom(64)[0].decode().strip()
            except socket.timeout: pass
    finally: s.close()
host=discover(); print('host=',host)
for port in (8000,8001):
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.bind(('0.0.0.0',0)); s.settimeout(1); got=False
    for _ in range(10):
        s.sendto(b'hello',(host,port))
        try:
            data,addr=s.recvfrom(100000); print('port',port,'received_bytes',len(data)); got=True; break
        except socket.timeout: pass
    print('port',port,'success=',got); s.close()
