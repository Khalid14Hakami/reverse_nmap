#!/usr/bin/env python3
 
import sys, socket, json, logging, os
from daemon import daemon
 

class ClientDaemon(daemon):
        logging_level = 30 
        logging.basicConfig(level = logging.DEBUG, filename = '/tmp/client_daemon.log', filemode='w')
        logger = logging.getLogger('client')

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
                                self.execute(data)

                                replay = { "message": "data received"}
                                replay = json.dumps(replay)
                                conn.sendall(bytes(replay,encoding="utf-8"))
            except Exception as e:
                print(e)
                self.logger.debug('at connect level')
                self.logger.exception(e)



            finally:
                s.close()
                return data
        
        def execute(self, json_command):
            file = json_command["script_path"]
            try:
                os.system(file)
            except Exception as e:
                self.logger.debug('at connect execution')
                self.logger.exception(e)
            return True
 
if __name__ == "__main__":


        daemon = ClientDaemon('/tmp/client_daemon.pid')

        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        print('daemon started')
                        daemon.start()
                        # daemon.log.debug('daemon started')
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