import socket, serial, time
p=serial.Serial('COM11',115200,timeout=0.1)
p.dtr=False; p.rts=True; time.sleep(0.2); p.rts=False; time.sleep(4)
p.reset_input_buffer()
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.bind(('0.0.0.0',0)); s.setblocking(False)
for i in range(5):
    s.sendto(b'hello',('192.168.88.101',8001)); time.sleep(0.5)
print('local=',s.getsockname())
end=time.time()+8; serial_data=b''; got=False
while time.time()<end:
    serial_data += p.read(4096)
    try:
        data,addr=s.recvfrom(100000); got=True; print('UDP_RECEIVED',len(data),addr); break
    except BlockingIOError: pass
    except OSError: pass
    time.sleep(0.05)
print('serial=',serial_data.decode('utf-8','replace'))
print('udp_received=',got)
p.close(); s.close()
