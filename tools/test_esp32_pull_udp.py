import socket, time
host = '192.168.88.101'
port = 8001
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 0))
s.settimeout(15)
print('local=', s.getsockname())
print('sending hello to', host, port)
s.sendto(b'hello', (host, port))
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
