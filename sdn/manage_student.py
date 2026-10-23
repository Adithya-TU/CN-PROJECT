import sys
import subprocess

if len(sys.argv) != 3 or sys.argv[1] not in ("block", "unblock"):
    print("Usage: sudo python3 sdn/manage_student.py block|unblock <student_ip>")
    sys.exit(1)

action, student_ip = sys.argv[1], sys.argv[2]

if action == "block":
    command = [
        "sudo", "ovs-ofctl", "-O", "OpenFlow13", "add-flow", "s1",
        f"priority=100,ip,nw_src={student_ip},actions=drop"
    ]
else:
    command = [
        "sudo", "ovs-ofctl", "-O", "OpenFlow13", "del-flows", "s1",
        f"ip,nw_src={student_ip}"
    ]

try:
    subprocess.run(command, check=True)
    print(f"Student {student_ip}: {action} rule applied.")
except subprocess.CalledProcessError as error:
    print("Failed to update OpenFlow rules:", error)
    sys.exit(1)
