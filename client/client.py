
import socket
import json
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 5000

def main():
    with socket.create_connection((HOST, PORT)) as conn:
        stream = conn.makefile("r", encoding="utf-8")
        exam = json.loads(stream.readline())
        answers = []
        print("\nONLINE EXAMINATION\n")
        for i, q in enumerate(exam["questions"], 1):
            print(f"\n{i}. {q['q']}")
            for j, option in enumerate(q["options"], 1):
                print(f"  {j}. {option}")
            while True:
                try:
                    choice = int(input("Your answer (1-4): "))
                    if 1 <= choice <= len(q["options"]):
                        answers.append(choice - 1)
                        break
                except ValueError:
                    pass
                print("Enter a valid option.")
        conn.sendall((json.dumps({"answers": answers}) + "\n").encode())
        result = json.loads(stream.readline())
        print(f"\nResult: {result['score']}/{result['total']}")

if __name__ == "__main__":
    main()
