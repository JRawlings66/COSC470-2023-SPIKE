import traceback
import sys
import os
# import credentials # ssh/db credentials in a separate file
from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder
from sqlalchemy.exc import ( #sqlalchemy common exceptions
    SQLAlchemyError,
    DataError,
    DatabaseError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
    TimeoutError,
) 

class TestException(Exception):
    def __init__(self, problems):
        message = "Primary key violation for the following rows:\n"
        for problem in problems:
            message += f"  {problem}\n"
        super().__init__(message)

# 4 databases
db = "dbs12118247"

try:
    print(f"Connecting to SSH...")
    with SSHTunnelForwarder(
        ('access975536837.webspace-data.io', 22),  # server ip, ssh port
        ssh_username='u113494172',  # shell username
        ssh_password='COSC-470-spike',  # shell password
        # ssh_pkey=credentials.key_path,  # path to private key file
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