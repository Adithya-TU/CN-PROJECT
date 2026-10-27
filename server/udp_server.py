import json
import socket

HOST = "0.0.0.0"
PORT = 5001

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, PORT))
        print(f"UDP status server listening on {HOST}:{PORT}")

        while True:
            data, addr = server.recvfrom(4096)
            try:
                request = json.loads(data.decode("utf-8"))
                response = {
                    "status": "online",
                    "service": "Online Examination Network",
                    "request": request
                }
            except (UnicodeDecodeError, json.JSONDecodeError):
                response = {"status": "error", "message": "Send a valid JSON request"}

            server.sendto(json.dumps(response).encode("utf-8"), addr)
            print("Replied to:", addr)

if __name__ == "__main__":
    main()
