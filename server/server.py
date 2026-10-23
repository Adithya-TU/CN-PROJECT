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
        with conn:
            stream = conn.makefile("r", encoding="utf-8")
            exam = {
                "type": "exam",
                "questions": [{"q": q["q"], "options": q["options"]} for q in questions],
                "duration": 120
            }
            conn.sendall((json.dumps(exam) + "\n").encode())

            line = stream.readline()
            if not line:
                print("Client disconnected before submitting:", addr)
                return

            submission = json.loads(line)
            answers = submission.get("answers", [])

            if not isinstance(answers, list):
                raise ValueError("Answers must be a list")

            score = sum(
                1 for i, q in enumerate(questions)
                if i < len(answers)
                and isinstance(answers[i], int)
                and not isinstance(answers[i], bool)
                and answers[i] == q["answer"]
            )

            with lock:
                results[f"{addr[0]}:{addr[1]}"] = score

            response = {
                "type": "result",
                "score": score,
                "total": len(questions)
            }
            conn.sendall((json.dumps(response) + "\n").encode())

    except (OSError, ValueError, json.JSONDecodeError) as e:
        print("Client error:", addr, e)
    finally:
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
