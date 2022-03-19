import socket
from scapy.all import *
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
s.bind(('0.0.0.0', 1337))
while True:
    # packet = s.recvfrom(65535)[0].decode()    #decode packet
    # print(packet)   #print packet to read
    packet = s.recvfrom(2000)
    packet = packet[0]
    p = IP(packet)
    
    ip = IP(src=p['IP'].dst, dst=p['IP'].src)/TCP(
    flags='A',
    sport=p['TCP'].dport,
    dport=p['TCP'].sport,
    seq = 0,
    ack = p['TCP'].seq + 1,
    )
    sr(ip, verbose=20)