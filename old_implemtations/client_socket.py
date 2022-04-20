import socket , json
print(socket.gethostname() )
HOST = "" 
PORT = 5432  # Port to listen on (non-privileged ports are > 1023)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    
                    data = data.decode("utf-8")
                    print(data)

                    replay = { "message": "data received"}
                    replay = json.dumps(replay)
                    conn.sendall(bytes(replay,encoding="utf-8"))
                    


finally:
    s.close()