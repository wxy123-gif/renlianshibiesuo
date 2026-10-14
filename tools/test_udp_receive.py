import socket, serial, time
p = serial.Serial('COM11', 115200, timeout=0.2)
p.dtr = False
p.rts = True
time.sleep(0.2)
p.rts = False
p.close()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 9091))
s.settimeout(15)
print('waiting for UDP 9091...')
try:
    data, addr = s.recvfrom(100000)
    print('received=True')
    print('bytes=', len(data))
    print('sender=', addr)
except Exception as e:
    print('received=False')
    print('error=', e)
finally:
    s.close()
