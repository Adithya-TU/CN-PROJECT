
import socket
import threading
import json

HOST = "0.0.0.0"
PORT = 5000
questions = [
    {"q": "What does TCP stand for?", "options": ["Transfer Control Protocol", "Transmission Control Protocol", "Transport Connection Process", "Terminal Control Protocol"], "answer": 1},
    {"q": "Which layer does IP operate at?", "options": ["Application", "Transport", "Network", "Session"], "answer": 2},
    {"q": "Which protocol is connection-oriented?", "options": ["UDP", "IP", "TCP", "ICMP"], "answer": 2},
    {"q": "What does DNS translate?", "options": ["IP addresses to MAC addresses", "Domain names to IP addresses", "Ports to processes", "Files to packets"], "answer": 1},
    {"q": "Which protocol is commonly used to transfer web pages securely?", "options": ["HTTP", "FTP", "HTTPS", "ARP"], "answer": 2}
]
results = {}
lock = threading.Lock()

def handle_client(conn, addr):
    score = 0
    try:
        stream = conn.makefile("r", encoding="utf-8")
        conn.sendall((json.dumps({"type": "exam", "questions": [{ "q": x["q"], "options": x["options"]} for x in questions], "duration": 120}) + "\n").encode())
        line = stream.readline()
        if not line:
            return
        submission = json.loads(line)
        answers = submission.get("answers", [])
        score = sum(1 for i, q in enumerate(questions) if i < len(answers) and answers[i] == q["answer"])
        with lock:
            results[addr[0] + ":" + str(addr[1])] = score
        conn.sendall((json.dumps({"type": "result", "score": score, "total": len(questions)}) + "\n").encode())
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print("Client error:", addr, e)
    finally:
        conn.close()
        print("Finished:", addr, "Score:", score)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Exam server listening on {HOST}:{PORT}")
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
