#!/usr/bin/env python3
 
from itertools import count
import sys, socket, json, logging, os
from time import sleep
from daemon import daemon
import subprocess
import ast
from scapy.all import *
import multiprocessing

 

class ClientDaemon(daemon):
    logging_level = 30 
    logging.basicConfig(level = logging.DEBUG, filename = '/tmp/client_daemon.log', filemode='w')
    logger = logging.getLogger('client')
    hostname = socket.gethostname()
    def run(self):
        self.register()
        self.connect()

    def connect(self):
        HOST = "" 
        PORT = 5432  # Port to listen on (non-privileged ports are > 1023)

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen()
                print(('daemon started'))
                self.logger.debug('daemon listening on port '+ str(PORT))

                while True:
                    conn, addr = s.accept()
                    with conn:
                        print(f"Connected by {addr}")
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            
                            data = data.decode("utf-8")

                            self.logger.debug('received the following:')
                            self.logger.debug(data)
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

    def launch_server(self, test_istruction):
        logging_level = 30 
        logging.basicConfig(level = logging.DEBUG, filename = '/tmp/server.log', filemode='w')
        logger = logging.getLogger('server')
        logger.debug("logger started")

        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        s.bind(('0.0.0.0', 1337))
 
        logger.debug(">>>>>>>>>>>>>>>>>>>")
        logger.debug(test_istruction)
        logger.debug("<<<<<<<<<<<<<<<<<<<")

        try:
            counter = 0
            while not eval(test_istruction["termiatin_condition"]):
                packet = s.recv(2000)
                logger.debug('this what we got:')
                logger.debug("".join(map(chr, bytes(packet[0]))))
                p = packet[0]
                logger.debug(type(packet))
                p = IP(packet)
                # if Raw in packet:
                #     load = packet[Raw].load
                #     print(load)
                logger.debug(p.summary())

                for state in test_istruction["states"]:
                    logger.debug(state)
                    if eval(state[0]):
                        logger.debug(state[0])

                        for step in state[1]:
                            logger.debug(step)
                            exec(test_istruction["steps"][int(step)])


                    logger.debug ("%s\n" % (p[IP].summary()))
                count = count + 1 
                        
        except Exception as e:
            print(e)
            logger.exception(e)
        
    
    def execute(self, json_command):
        
        try:
            if json_command["script_path"]:
                file = json_command["script_path"]
                subprocess.Popen(file)
            elif json_command["test_istruction"]:
                test = json_command["test_istruction"]
                test_server = multiprocessing.Process(target=self.launch_server, args=[test])
                test_server.start()
            # test_server.join()
        except Exception as e:
            self.logger.exception(e)
            return(e)
        return True


    def register(self):
        self.logger.debug("start registration")
        snooz = False
        try: 
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection = s.connect(("controller", 4444))
            while True:
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
                if snooz: 
                    sleep(300) 
                    snooz = False
                else: 
                    sleep(5)
            
            
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