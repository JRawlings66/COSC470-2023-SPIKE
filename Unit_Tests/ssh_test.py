import traceback
import sys
import os

# import credentials # ssh/db credentials in a separate file
from sshtunnel import SSHTunnelForwarder


class TestException(Exception):
    def __init__(self, problems):
        message = "Primary key violation for the following rows:\n"
        for problem in problems:
            message += f"  {problem}\n"
        super().__init__(message)


# 4 databases
db = ""

try:
    print(f"Connecting to SSH...")
    with SSHTunnelForwarder(
        ("hostname", 22),  # server ip, ssh port
        ssh_username="sh_name",  # shell username
        ssh_password="sh_pass",  # shell password
        remote_bind_address=(
            "127.0.0.1",
            3306,
        ),  # localhost, mariadb default port
    ) as tunnel:
        tunnel.start()
        print(f"local_bind_port: {tunnel.local_bind_port}")
        print("SSH Connection Success")
except Exception:
    print(traceback.format_exc())
    print("An SSH connection error occurred.")
