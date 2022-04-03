import socket
from scapy.all import *
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
s.bind(('0.0.0.0', 1337))
# mystream=StreamSocket(s)

test_istruction= {
    "condition": "p['TCP'].dport == 80",
    "steps": [
        """
print('this is a test', p['TCP'].dport)
ip = IP(src=p['IP'].dst, dst=p['IP'].src)/TCP(
flags='SA',
sport=p['TCP'].dport,
dport=p['TCP'].sport,
seq = 0,
ack = p['TCP'].seq + 1,
)
pair = sr1(ip, verbose=30)"""
    ], 
    "states": ("p['TCP'].flags == 'S'", [1, 2])
}

while True:
    # packet = s.recvfrom(65535)[0].decode()    #decode packet
    # print(packet)   #print packet to read
    packet = s.recv(2000)
    print('this what we got:')
    print("".join(map(chr, bytes(packet[0]))))
    p = packet[0]
    print(type(packet))
    p = IP(packet)
    # if Raw in packet:
    #     load = packet[Raw].load
    #     print(load)
    print(p.summary())
    if True: # p['TCP'].flags == 'S':
        for state in test_istruction["states"]:
            if eval(state[0]):
                print("steps")
                print(state[1])
                for step in list(state[1]):
                    print(step)
                    exec(test_istruction["steps"][int(step)])


            print ("%s\n" % (p[IP].summary()))