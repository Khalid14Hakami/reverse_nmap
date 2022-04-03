"""
Simple concurrent TCP server
reading from several sockets
using select()
"""
from atexit import register
import socket
import select
import multiprocessing
import json

PORT=4444
HOST=""



class Registrar():


    def __init__(self):
        manager = multiprocessing.Manager()
        global workers_list 
        workers_list = manager.list()
        
    def get_workers(self):
        return workers_list
    
    def refresh_worker_list():
        pass

    def launch_server(self, shared_data):

        srv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        srv.bind((HOST,PORT))
        srv.listen(1)

        #associate each socket to its address info
        clisocks={}
        end="not yet"

        while True:
            r,w,x=select.select([srv]+list(clisocks.keys()),[],[])
            
            if srv in r:
                conn,addr=srv.accept()
                print ("new connection from {}".format(addr))
                clisocks[conn]=addr
            
            for conn in [i for i in r if i!=srv]:
                print("There is something to read from {}".format(conn))
                data=conn.recv(1024)
                if data:
                    try:
                        registered = False
                        data = json.loads(data.decode())
                        if data["hostname"]:
                            for host in workers_list:
                                if data["hostname"] == host["hostname"]:
                                    host["ip"]= conn.getpeername()[0] # update with new ip 
                                    registered = True

                            data["ip"]= conn.getpeername()[0]
                        if not registered:
                            workers_list.append(data)
                            print(workers_list)
                            conn.send(str(workers_list).encode('utf-8'))
                    except Exception as e:
                        conn.send(str(e).encode('utf-8'))
                else:
                    print("dropped connection from {}".format(clisocks[conn]))
                    clisocks.pop(conn)

                
        # time to nicely close all the sockets
        for conn in r:
                conn.close()
        # Was it a good idea ?       
        print("over and out") 

    def start(self):

        register = multiprocessing.Process(target=self.launch_server, args=[workers_list])
        register.start()
        
        return register


       
                         