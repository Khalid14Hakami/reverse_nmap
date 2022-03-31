import socket
from scapy.all import *
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
s.bind(('0.0.0.0', 1337))
# mystream=StreamSocket(s)

test_istruction= {
    "condition": "p['TCP'].dport == 80",
    "steps": [
        "print('this is a test', p['TCP'].dport)"
    ]
}

while True:
    # packet = s.recvfrom(65535)[0].decode()    #decode packet
    # print(packet)   #print packet to read
    packet = s.recv(2000)
    print('this what we got:')
    print("".join(map(chr, bytes(packet[0]))))
    p = packet[0]
    print(type(p))
    # p = IP(packet)
    if Raw in packet:
        load = packet[Raw].load
        print(load)
    print(packet.summary())
    if True: # p['TCP'].flags == 'S':
        ip = IP(src=p['IP'].dst, dst=p['IP'].src)/TCP(
        flags='SA',
        sport=p['TCP'].dport,
        dport=p['TCP'].sport,
        seq = 0,
        ack = p['TCP'].seq + 1,
        )

        eval(test_istruction.steps[0])
        pair, unans = sr1(ip, verbose=30)
        print (pair)
    

    print ("%s\n" % (p[IP].summary()))