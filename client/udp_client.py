import json
import socket
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 5001

def main():
    request = {"type": "status", "client": "student"}
    message = json.dumps(request).encode("utf-8")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.settimeout(3)
        try:
            client.sendto(message, (HOST, PORT))
            data, addr = client.recvfrom(4096)
            print("Server:", addr)
            print("Response:", data.decode("utf-8"))
        except socket.timeout:
            print("No response: check the server IP, port, and whether the UDP server is running.")
            sys.exit(1)
        except OSError as e:
            print("Network error:", e)
            sys.exit(1)

if __name__ == "__main__":
    main()
