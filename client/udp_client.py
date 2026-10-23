import socket
import json
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "10.0.0.1"
PORT = 5001

request = {"request": "status"}

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    client.settimeout(3)
    client.sendto(json.dumps(request).encode(), (HOST, PORT))
    try:
        data, addr = client.recvfrom(1024)
        print("Server response:", json.loads(data.decode()))
    except socket.timeout:
        print("No response from UDP server")
