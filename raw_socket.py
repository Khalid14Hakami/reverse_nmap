import socket
from scapy.all import *
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
s.bind(('0.0.0.0', 1337))
mystream=StreamSocket(s)
while True:
    # packet = s.recvfrom(65535)[0].decode()    #decode packet
    # print(packet)   #print packet to read
    packet = mystream.recv(2000)
    print('this what we got:')
    print("".join(map(chr, bytes(packet[0]))))
    p = packet
    # p = IP(packet)
    print(packet.summary())
    if True: # p['TCP'].flags == 'S':
        ip = IP(src=p['IP'].dst, dst=p['IP'].src)/TCP(
        flags='SA',
        sport=p['TCP'].dport,
        dport=p['TCP'].sport,
        seq = 0,
        ack = p['TCP'].seq + 1,
        )
        pair, unans = sr1(ip, verbose=30)
        print (pair)
    

    print ("%s\n" % (p[IP].summary()))