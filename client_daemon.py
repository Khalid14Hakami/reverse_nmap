#!/usr/bin/env python3
 
from datetime import datetime
from itertools import count
import sys, socket, json, logging, os
import time, datetime
from daemon import daemon
import subprocess
import ast
from scapy.all import *
from queue import Queue
import threading
import multiprocessing
import psutil


print_lock = threading.Lock() # TODO: is there a better way? 

class StatefulSocket(threading.Thread):
    def __init__(self, queue, server_state_machine, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.state = "init"
        self.timeout = 120 # in seconds
        self.states = server_state_machine
        self.queue = queue
        self.state_start_time = datetime.datetime.now()
        # logging.basicConfig(level = logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', filename = '/tmp/client_daemon.log', filemode='w')
        self.logger = logging.getLogger('thread-'+threading.currentThread().getName())

    def run(self):
        self.logger.debug(threading.currentThread().getName())
        while True:
            try:
                self.logger.debug(" im a liveeee")
                if self.check_timeout(): # to end the thread (state for this connectio) after timeout 
                    self.logger.debug(" timeout..... bye")
                    break
                val = self.queue.get()
                if val is None:   # TODO: change to state termination condition 
                    return
                self.respond(val)
            except Exception as e: 
                self.logger.exception(e)

    def respond(self, message):
        with print_lock:
            self.logger.debug("Received {}".format(message.summary()))
            for transition in self.states["states"][self.state]["transitions"]:
                p = message # this is the packet parsed at parent as a scapy packet 
                if eval(transition["transition_condition"]):
                    exec(transition["transition_response"])
                    print("from this state "+ self.state + "to "+ transition["next_state"])
                    self.state = transition["next_state"]
                    self.state_start_time = datetime.datetime.now()
                    break # dont check other transitions 
    
    def check_timeout(self):
        self.logger.debug(self.state_start_time)
        self.logger.debug((datetime.datetime.now() - self.state_start_time))
        self.logger.debug(float(self.states["states"][self.state]["timeout"]))
        return (datetime.datetime.now() - self.state_start_time).total_sconds() > float(self.states["states"][self.state]["timeout"])

class ClientDaemon(daemon):
    logging_level = 30 
    logging.basicConfig(level = logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', filename = '/tmp/client_daemon.log', filemode='w')
    logger = logging.getLogger('client')
    hostname = socket.gethostname()
    def run(self):
        self.register()
        self.connect()

    def connect(self):
        """
        this funtion is to open a socket to receive commands from the controller 
        """
        HOST = "" 
        PORT = 5432  # Port to listen on (non-privileged ports are > 1023)

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                s.bind((HOST, PORT))
                s.listen(1)
                print(('daemon started'))
                self.logger.debug('daemon listening on port '+ str(PORT))

                while True:
                    conn, addr = s.accept()
                    with conn:
                        print(f"Connected by {addr}")
                        while True:
                            data = conn.recv(5120)
                            if not data:
                                break
                            
                            data = data.decode("utf-8")

                            self.logger.debug('received the following:')
                            self.logger.debug(data)
                            
                            if len(data)>5:
                                data = json.loads(data)
                                result = self.execute(data)
                            
                            replay = { "message": result}
                            replay = json.dumps(replay)
                            conn.sendall(bytes(replay,encoding="utf-8"))
                            
        except Exception as e:
            print(e)
            self.logger.exception(e)



        finally:
            s.close()
            return data

    def launch_server(self, state_machine):
        logging_level = 30 
        logger = logging.getLogger('server')
        logger.debug("server logger started")
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        s.bind(('0.0.0.0', 1337))
 
        logger.debug(">>>>>>>>>>>>>>>>>>>")

        logger.debug(state_machine)
        logger.debug("<<<<<<<<<<<<<<<<<<<")

        threads = []
        connections = {}
        # TODO: clean up dead threads
        # TODO: use timeout

        try:
            counter = 0
            # TODO: check for recieving full packet using fragment number 
            while 1:
                logger.debug("trying to get message:   >>>>>>>>>>>> ^^^^^^^^^^^^^^^^ <<<<<<<<<<<")

                packet, address = s.recvfrom(2000)
    
                p = packet[0]
                p = IP(packet)

                logger.debug(p.summary())
                client_address = str(p[IP].src) + ":" + str(p[TCP].sport)
                logger.debug("got data from: " + client_address)
                logger.debug("connections.keys()       : 888888888")
                logger.debug(connections.keys())
                logger.debug("is it alive?????????")
                if client_address in connections.keys():
                    logger.debug(connections[client_address].is_alive())        
                if client_address in connections.keys() and connections[client_address].is_alive():
                    logger.debug("client exsit:   >>>>>>>>>>>> ^^^^^^^^^^^^^^^^ <<<<<<<<<<<")

                    connections[client_address].queue.put(p)
                else:
                    logger.debug("new client:   >>>>>>>>>>>> ^^^^^^^^^^^^^^^^ <<<<<<<<<<<")

                    q = Queue()
                    connections[client_address] = StatefulSocket(q, state_machine)
                    connections[client_address].start()
                    connections[client_address].queue.put(p)

                counter = counter + 1 

                        
        except Exception as e:
            print(e)
            logger.exception(e)
        
    
    def execute(self, json_command):
        
        try:
            if "script_path" in json_command:
                file = json_command["script_path"]
                subprocess.Popen(file)
            elif "state_machine" in json_command:
                # kill all subprocesses if any
                current_process = psutil.Process()
                children = current_process.children(recursive=True)
                for child_prc in children:
                    child_prc.terminate()
                state_machine = json_command["state_machine"]
                test_server = multiprocessing.Process(target=self.launch_server, args=[state_machine])
                test_server.daemon = True 
                test_server.start()
            # test_server.join()
        except Exception as e:
            self.logger.exception(e)
            return(e)
        return True


    def register(self):
        self.logger.debug("start registration")
        snooz = False
        while True:
            try: 
            
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection = s.connect(("controller", 4444))
                self.logger.debug(' registration for     '+ str(socket.gethostname()))

                
                data = {"hostname": self.hostname}
                s.sendall(bytes(json.dumps(data),encoding="utf-8"))
                ans = s.recv(1024)
                self.logger.debug(ans)
                ans = json.loads(ans.decode().replace("\'", "\""))
                self.logger.debug(ans)
                for host in ans:
                    self.logger.debug("host >>> " + host["hostname"])
                    self.logger.debug(" >>>>>> socket.gethostname(): ")
                    self.logger.debug(" socket +++ " + socket.gethostname())
                    if host["hostname"] == self.hostname:
                        snooz = True
                        return True
                if snooz: 
                    time.sleep(300) 
                    snooz = False
                else: 
                    time.sleep(5)
                
            
            except Exception as e: 
                self.logger.exception(e)
                return(e)
 
if __name__ == "__main__":


    daemon = ClientDaemon('/tmp/client_daemon.pid')


    if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                    daemon.start()
                    daemon.logger.debug('daemon started')
            elif 'stop' == sys.argv[1]:
                    daemon.stop()
            elif 'restart' == sys.argv[1]:
                    daemon.restart()
            else:
                    print ("Unknown command")
                    sys.exit(2)
            sys.exit(0)
    else:
            print ("usage: %s start|stop|restart" % sys.argv[0])
            sys.exit(2)