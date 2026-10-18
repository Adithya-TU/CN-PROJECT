import socket
import json

HOST = "0.0.0.0"
PORT = 5001

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind((HOST, PORT))
    print(f"UDP status server listening on port {PORT}", flush=True)
    while True:
        data, addr = server.recvfrom(1024)
        try:
            request = json.loads(data.decode())
            response = {
                "status": "online",
                "service": "Online Examination Network",
                "request": request.get("request", "status")
            }
        except (ValueError, UnicodeDecodeError):
            response = {"status": "error", "message": "Invalid request"}
        server.sendto(json.dumps(response).encode(), addr)
        print(f"UDP request from {addr}", flush=True)
