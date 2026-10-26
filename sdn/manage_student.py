import argparse
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["block", "unblock"])
    parser.add_argument("ip")
    parser.add_argument("--switch", default="s1")
    args = parser.parse_args()

    if args.action == "block":
        command = [
            "sudo", "ovs-ofctl", "-O", "OpenFlow13", "add-flow",
            args.switch,
            f"priority=100,ip,nw_src={args.ip},actions=drop"
        ]
    else:
        command = [
            "sudo", "ovs-ofctl", "-O", "OpenFlow13", "del-flows",
            args.switch,
            f"ip,nw_src={args.ip}"
        ]

    try:
        subprocess.run(command, check=True)
        print(f"Successfully executed {args.action} for {args.ip}")
    except subprocess.CalledProcessError:
        print("Command failed. Check that Mininet and switch s1 are running.")
        sys.exit(1)

if __name__ == "__main__":
    main()
