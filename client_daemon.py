#!/usr/bin/env python3
 
import sys, socket, json, logging, os
from daemon import daemon
 

class ClientDaemon(daemon):
        logging_level = 30 
        log = logging.basicConfig(level = logging.DEBUG, filename = '/tmp/client_daemon.log', filemode='w')

        def run(self):
            self.connect()

        def connect(self):
            HOST = "" 
            PORT = 5432  # Port to listen on (non-privileged ports are > 1023)

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((HOST, PORT))
                    s.listen()
                    self.log.DEBUG('daemon listening on port '+ str(PORT))

                    while True:
                        conn, addr = s.accept()
                        with conn:
                            print(f"Connected by {addr}")
                            while True:
                                data = conn.recv(1024)
                                if not data:
                                    break
                                
                                data = data.decode("utf-8")

                                self.log.DEBUG('received the following:')
                                self.log.DEBUG(data)

                                self.execute(data)

                                replay = { "message": "data received"}
                                replay = json.dumps(replay)
                                conn.sendall(bytes(replay,encoding="utf-8"))

            finally:
                s.close()
                return data
        
        def execute(json_command):
            file = json_command["script_path"]
            try:
                os.system(file)
            except Exception as e:
                self.log.DEBUG(e)
            return True
 
if __name__ == "__main__":


        daemon = ClientDaemon('/tmp/client_daemon.pid')

        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                        daemon.log.DEBUG('daemon started')
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