from registrar import *
from cmd import Cmd
import os, sys
 
class MyPrompt(Cmd):
    def do_exit(self, inp):
        print("Bye")
        return True

    def do_add(self, inp):
        print("Adding '{}'".format(inp))

    def do_list(self, inp):
        print(reg.get_workers())
        

    def do_run_test(self, inp):
        print(os.path.isfile(inp))
        print(os.path.splitext(inp)[1])
        if  os.path.isfile(inp) and os.path.splitext(inp)[1] == '.json':
            # load json from file
            scenario = self.get_scenario(inp)
            server_settings = scenario['server_setting']
            clients_settings = scenario['clients_settings']
            sniffer_settings = scenario['sniffer_settings']

            server_status = self.prepare_server(server_settings)
            # snfiffer_status = prepare_sniffer(sniffer_settings)

            if server_status and snfiffer_status:
                trigger_clients(clients_settings)
        else:
            print ("file format not suported")
            # sys.exit(2)
        # sys.exit(0)
        print(reg.get_workers())


    def get_scenario(self, scenario_name):
        """ this function get the scenario configuration from json file by name"""
        f = open(scenario_name)
        return json.load(f)

    def prepare_server(self, server_settings):
        """
        this function takes the server setting 
        from the scenario config and prepare server 
        by contacting the server daemon
        """
        result = self.connect(server_settings)
        if result['message'] == True:
            return True
        else:
            print('server did not start successfully')
            print(result)
        # sys.exit(2) 

    def connect(self, configs):
        HOST = configs['HOST'] # socket.gethostname() 
        PORT = 5432  # Port to listen on (non-privileged ports are > 1023)
        ans = ""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                

                print(f"Connected to {HOST}")

                data = {
                    "script_path": configs['script_path'],
                    "test_istruction": configs['test_istruction']
                }
                data = json.dumps(data)
                s.sendall(bytes(data,encoding="utf-8"))

                ans = s.recv(1024)
                ans = ans.decode("utf-8")
                ans = json.loads(ans)
                print(ans) 
        except Exception as e:
            print(e)       
        finally:
            s.close()
            print ("answer: \n", ans )
            return ans  
 



if __name__ == "__main__":
    print("firing up rigestrar")
    reg = Registrar()
    registrar_process = reg.start()

    MyPrompt().cmdloop()
    print("after")
    registrar_process.join()

#    print (reg.checkstatus()) 
