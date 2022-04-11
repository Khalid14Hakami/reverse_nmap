import threading
import time, socket
from scapy.all import *
from queue import Queue

print_lock = threading.Lock()

class StatefulSocket(threading.Thread):
    def __init__(self, queue, socket, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.state = "init"
        self.socket = socket
        self.queue = queue
        self.daemon = True
        self.receive_messages = args[0]

    def run(self):
        print (threading.currentThread().getName(), self.receive_messages)
        val = self.queue.get()
        self.do_thing_with_message(val)

    def do_thing_with_message(self, message):
        if self.receive_messages:
            with print_lock:
                print (threading.currentThread().getName(), "Received {}".format(message))

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
            p = packet[0]
            p = IP(packet)
            # if Raw in packet:
            #     load = packet[Raw].load
            #     print(load)
            print(p.summary())
            print("got data from: ", address)

            # for state in test_istruction["states"]:
            #     logger.debug(state)
            #     if eval(state[0]):
            #         logger.debug(state[0])

            #         for step in state[1]:
            #             logger.debug(step)
            #             exec(test_istruction["steps"][int(step)])


            #     logger.debug ("%s\n" % (p[IP].summary()))
            counter = counter + 1 
                        
    except Exception as e:
        print(e)

    # for t in range(10):
    #     q = Queue()
    #     threads.append(MyThread(q, args=(t % 2 == 0,)))
    #     threads[t].start()
    #     time.sleep(0.1)

    # for t in threads:
    #     t.queue.put("Print this!")

    # for t in threads:
    #     t.join()