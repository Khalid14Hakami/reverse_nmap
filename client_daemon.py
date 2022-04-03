#!/usr/bin/env python3
 
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

    def launch_Server(self, test_istruction):
        


        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        s.bind(('0.0.0.0', 1337))
        # mystream=StreamSocket(s)

        # test_istruction= {
        #     "condition": "p['TCP'].dport == 80",
        #     "steps": [
        #         """
        # print('this is a test', p['TCP'].dport)
        # ip = IP(src=p['IP'].dst, dst=p['IP'].src)/TCP(
        # flags='SA',
        # sport=p['TCP'].dport,
        # dport=p['TCP'].sport,
        # seq = 0,
        # ack = p['TCP'].seq + 1,
        # )
        # pair = sr1(ip, verbose=30)""",
        # """
        # print('this is a step 2', p['TCP'].dport)
        # ip = IP(src=p['IP'].dst, dst=p['IP'].src)/TCP(
        # flags='A',
        # sport=p['TCP'].dport,
        # dport=p['TCP'].sport,
        # seq = p['TCP'].seq ,
        # ack = p['TCP'].seq + p['TCP'].len,
        # )
        # pair = sr1(ip, verbose=30, timeout= 3)"""
        #     ], 
        #     "states": [
        #             ("p['TCP'].flags == 'S'", "[0]"), 
        #             ]
        # }

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
                        for step in ast.literal_eval(state[1]):
                            print(step)
                            exec(test_istruction["steps"][int(step)])


                    print ("%s\n" % (p[IP].summary()))
        
    
    def execute(self, json_command):
        file = json_command["script_path"]
        test = json_command["test_istruction"]
        register = multiprocessing.Process(target=self.launch_server, args=[test])
        try:
            # subprocess.Popen(file)
            register.start()
            register.join()
        except Exception as e:
            self.logger.exception(e)
            return(e)
        return True


    def register(self):
        self.logger.debug("start registration")
        try: 
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection = s.connect(("controller", 4444))
            while True:
                self.logger.debug(' registration for on port '+ str(socket.gethostname()))
                self.logger.debug(connection)
                self.logger.debug(s)
                
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
                        return True
                sleep(5)
            
        except Exception as e: 
            self.logger.exception(e)
            return(e)
 
if __name__ == "__main__":


    daemon = ClientDaemon('/tmp/client_daemon.pid')


    if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                    if daemon.register():
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