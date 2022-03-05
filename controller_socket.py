from cgitb import Hook
from json.tool import main
from site import execsitecustomize
import socket, json
import sys

def connect(configs):
    HOST = configs['HOST'] # socket.gethostname() 
    PORT = 5432  # Port to listen on (non-privileged ports are > 1023)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            

            print(f"Connected to {HOST}")

            data = {
                "script_path": configs['script_path']
            }
            data = json.dumps(data)
            s.sendall(bytes(data,encoding="utf-8"))

            ans = s.recv(1024)
            ans = ans.decode("utf-8")
            ans = json.loads(ans)
            print(ans)        
    finally:
        s.close()
        return ans


def get_scenario(scenario_name):
    """ this function get the scenario configuration from json file by name"""
    f = open(scenario_name)
    return json.load(f)
     
 

def prepare_server(server_settings):
    """
    this function takes the server setting 
    from the scenario config and prepare server 
    by contacting the server daemon
    """
    result = connect(server_settings)
    if result['message'] == True:
        return True
    else:
        print('server did not start successfully')
        print(result)
        sys.exit(2)

def prepare_sniffer(siffer_setting):
    """
    this function contact the sniffer daemon to prepare sniffing based on the scenario
    """
    return True

def trigger_clients(clients_settings):
    """
        this contact clients' deamons to 
        trigger scenario communication to target server
    """
    result = connect(clients_settings)
    if result['message'] == True:
        return True
    else:
        print('server did not start successfully')
        print(result)
        sys.exit(2)


if __name__ == "__main__":

    if len(sys.argv) == 2:
        if  sys.argv[1] is 'json':
            # load json from file
            scenario = get_scenario(sys.argv[1])
            server_settings = scenario['server_setting']
            clients_settings = scenario['clients_settings']
            server_status = prepare_server(server_settings)
            snfiffer_status = prepare_sniffer(scenario)

            if server_status and snfiffer_status:
                trigger_clients(clients_settings)

        else:
            print ("file format not suported")
            sys.exit(2)
        sys.exit(0)
    else:
            print ("usage: %s [path_to_scenario_json_file]" % sys.argv[0])
            sys.exit(2)

