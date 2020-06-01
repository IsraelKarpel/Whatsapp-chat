import sys
from socket import socket, AF_INET, SOCK_DGRAM

s = socket(AF_INET, SOCK_DGRAM)
dest_ip = sys.argv[1]
dest_port = int(sys.argv[2])
server_send = (dest_ip, dest_port)
msg = raw_input()
while not msg == "4":
    s.sendto(msg, server_send)
    data, sender_info = s.recvfrom(2048)
    while data != "":
        print(data)
        data, sender_info = s.recvfrom(2048)
    msg = raw_input()
s.sendto(msg, server_send)
s.close()