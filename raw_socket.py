import socket
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
s.bind(('0.0.0.0', 1337))
while True:
    packet = s.recvfrom(65535)[0].decode()    #decode packet
    print(packet)   #print packet to read