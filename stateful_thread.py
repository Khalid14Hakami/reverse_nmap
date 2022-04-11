import threading
import time, socket
from scapy.all import *
from queue import Queue
import json

print_lock = threading.Lock()

class StatefulSocket(threading.Thread):
    def __init__(self, queue, socket, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.state = "init"
        global state_machine
        f = open('staeful.json')
        state_machine = json.load(f)
        f.close()
        self.states = state_machine.copy()
        self.socket = socket
        self.queue = queue

    def run(self):
        print (threading.currentThread().getName())
        while True:
            val = self.queue.get()
            if val is None:   # TODO: change to if FIN 
                return
            self.do_thing_with_message(val)

    def do_thing_with_message(self, message):
        with print_lock:
            print (threading.currentThread().getName(), "Received {}".format(message.summary()))
            print(state_machine)
            for transition in state_machine["states"][self.state]["transitions"]:
                if eval(transition["transiotion_condition"]):
                    exec(transition["transition_response"])
                    self.state = transition["next_state"]

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    s.bind(('0.0.0.0', 1337))
    threads = []
    connections = {}

    try:
        counter = 0
        while 1:
            packet, address = s.recvfrom(2000)
            print(packet)
            print(address)
            print(type(address))
            p = packet[0]
            p = IP(packet)

            print(p.summary())
            client_address = str(p[IP].src) + ":" + str(p[TCP].sport)
            print("got data from: ", client_address)


            if client_address in connections.keys() and connections[client_address].is_alive():
                connections[client_address].queue.put(p)
            else:
                q = Queue()
                connections[client_address] = StatefulSocket(q, str)
                connections[client_address].start()
                connections[client_address].queue.put(p)

            counter = counter + 1 
                        
    except Exception as e:
        print(e)
