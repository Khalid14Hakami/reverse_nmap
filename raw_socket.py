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
    if True: # p['TCP'].flags == 'S':
        ip = IP(src=p['IP'].dst, dst=p['IP'].src)/TCP(
        flags='SA',
        sport=p['TCP'].dport,
        dport=p['TCP'].sport,
        seq = 0,
        ack = p['TCP'].seq + 1,
        )
        pair, unans = sr(ip, verbose=30)
        if len(pair) != 1:
            print("We have received %s answers to the SYN pckt instead of 1.\nAborting", len(pair))
            exit()
        if str(pair[0][1][TCP].flags)=="SA":
            print("SYN ACK packet received")
            synackpkt=pair[0][1]
        else:
            print("Response to the SYN Packet had the %s flags instead of SYN ACK\n===>You probably forgot to launch your server. By default it should be on s3.net3.local, port 2000\n\"nc -l 2000\"\n\nAborting", str(pair[0][1][TCP].flags))
            exit()

    print ("%s\n" % (p[IP].summary()))