import socket, serial, time
# Normal reset so main.py starts.
p=serial.Serial('COM11',115200,timeout=0.1)
p.dtr=False; p.rts=True; time.sleep(0.2); p.rts=False
p.close(); time.sleep(4)
for port in (8000, 8001):
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(('0.0.0.0',0)); s.settimeout(10)
    s.sendto(b'hello',('192.168.88.101',port))
    try:
        data,addr=s.recvfrom(100000)
        print('port',port,'received_bytes',len(data),'sender',addr)
    except Exception as e:
        print('port',port,'FAILED',e)
    s.close()
