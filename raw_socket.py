import socket
from scapy.all import *
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
s.bind(('0.0.0.0', 1337))
while True:
    # packet = s.recvfrom(65535)[0].decode()    #decode packet
    # print(packet)   #print packet to read
    packet = s.recvfrom(2000)
    p = packet[0]
    
    ip = IP(src=p['IP'].dst, dst=p['IP'].src)/TCP(
        flags='A',
        sport=p['TCP'].dport,
        dport=p['TCP'].sport,
        seq = ackpkt['TCP'].seq + 1,
        ack = p['TCP'].seq + 1,
    )
    
    send(ip, verbose=scapy_verbose)