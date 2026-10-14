import serial,socket,time
p=serial.Serial('COM11',115200,timeout=0.1); p.dtr=False; p.rts=True; time.sleep(0.2); p.rts=False; p.close(); time.sleep(5)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.bind(('0.0.0.0',0)); s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1); s.settimeout(0.5)
found=None
for i in range(10):
    s.sendto(b'discover',('255.255.255.255',8888))
    try:
        data,addr=s.recvfrom(64); found=data.decode().strip(); print('found=',found,'from',addr); break
    except socket.timeout: pass
print('success=',bool(found)); s.close()
