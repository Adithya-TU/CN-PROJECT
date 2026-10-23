
import socket
import json
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 5000

def main():
    try:
        with socket.create_connection((HOST, PORT), timeout=10) as sock:
            stream = sock.makefile("r", encoding="utf-8")
            line = stream.readline()

            if not line:
                print("Server closed the connection without sending the exam.")
                return

            exam = json.loads(line)

            if exam.get("type") != "exam":
                print("Unexpected response from server.")
                return

            questions = exam.get("questions", [])
            answers = []

            print("\nONLINE EXAMINATION")
            print("------------------")

            for i, question in enumerate(questions, 1):
                print(f"\n{i}. {question['q']}")
                options = question.get("options", [])

                for j, option in enumerate(options, 1):
                    print(f" {j}. {option}")

                while True:
                    choice = input("Your answer (number): ").strip()

                    if choice.isdigit() and 1 <= int(choice) <= len(options):
                        answers.append(int(choice) - 1)
                        break

                    print(f"Enter a number from 1 to {len(options)}.")

            sock.sendall(
                (json.dumps({"answers": answers}) + "\n").encode("utf-8")
            )

            result_line = stream.readline()

            if not result_line:
                print("Server disconnected before returning the result.")
                return

            result = json.loads(result_line)

            if result.get("type") == "result":
                print(
                    f"\nYour score: {result.get('score', 0)}/"
                    f"{result.get('total', len(questions))}"
                )
            else:
                print("Unexpected result from server.")

    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        print("Could not complete the exam:", error)
        print("Check that the server is running and the server IP/port are correct.")

if __name__ == "__main__":
    main()

