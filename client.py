import socket
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
if sys.argv[2].__contains__('.'):
    ip = sys.argv[2]
    port = sys.argv[1]
else:
    port = sys.argv[2]
    ip = sys.argv[1]
if port > 65536 or port <1:
    sys.exit()
while True:
    nextCommand = input()
    s.sendto(nextCommand.encode('ascii'), (ip, int(port)))
    data, addr = s.recvfrom(1024)
    msg = data.decode('ascii')
    if msg == "disconnect":
        break
    else:
        if msg != "":
            print(msg)
s.close()