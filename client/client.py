import socket
import json
import sys
import time
import select


HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 5000


def timed_input(prompt, deadline):
    print(prompt, end="", flush=True)

    remaining = deadline - time.monotonic()

    if remaining <= 0:
        return None

    ready, _, _ = select.select([sys.stdin], [], [], remaining)

    if not ready:
        return None

    return sys.stdin.readline().strip()


def main():
    try:
        with socket.create_connection((HOST, PORT), timeout=10) as sock:
            sock.settimeout(None)
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
            duration = exam.get("duration", 120)
            answers = []
            deadline = time.monotonic() + duration
            timed_out = False

            print("\nONLINE EXAMINATION")
            print("------------------")
            print("Time limit:", duration, "seconds")

            for i, question in enumerate(questions, 1):
                if time.monotonic() >= deadline:
                    timed_out = True
                    break

                print(f"\n{i}. {question['q']}")
                options = question.get("options", [])

                for j, option in enumerate(options, 1):
                    print(f" {j}. {option}")

                while True:
                    choice = timed_input("Your answer (number): ", deadline)

                    if choice is None:
                        timed_out = True
                        break

                    if choice.isdigit() and 1 <= int(choice) <= len(options):
                        answers.append(int(choice) - 1)
                        break

                    print(f"Enter a number from 1 to {len(options)}.")

                if timed_out:
                    break

            if timed_out:
                print("\nTime limit exceeded!")
                print("Exam automatically stopped.")
                return

            sock.sendall((json.dumps({"answers": answers}) + "\n").encode("utf-8"))

            result_line = stream.readline()

            if not result_line:
                print("Server disconnected before returning the result.")
                return

            result = json.loads(result_line)

            if result.get("type") == "result":
                print("\nEXAMINATION RESULT")
                print("Score:", result.get("score", 0), "/", result.get("total", len(questions)))

                if "elapsed" in result:
                    print("Time taken:", result["elapsed"], "seconds")
            else:
                print("Unexpected result from server.")

    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print("Could not complete the exam:", error)
        print("Check that the server is running and the server IP/port are correct.")


if __name__ == "__main__":
    main()
