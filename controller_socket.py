from cgitb import Hook
import socket, json

HOST = 'c1' # socket.gethostname() 
PORT = 5432  # Port to listen on (non-privileged ports are > 1023)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        

        print(f"Connected to {HOST}")

        data = {
            "script_path": "/scripts/run_nc.sh",
            "job": "student"
        }

        data = json.dumps(data)
        s.sendall(bytes(data,encoding="utf-8"))

        ans = s.recv(1024)
        print(ans)        

finally:
    s.close()