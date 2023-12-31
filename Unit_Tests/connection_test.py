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
db = ""

try:
    print(f"Connecting to SSH...")
    with SSHTunnelForwarder(
        ('', 22),  # server ip, ssh port
        ssh_username='',  # shell username
        ssh_password='',  # shell password
        # ssh_pkey=credentials.key_path,  # path to private key file
        remote_bind_address=(
            "127.0.0.1",
            3306,
        ),  # localhost, mariadb default port
    ) as tunnel:
        tunnel.start()

        try:
            print("Connecting to database...")
            uri = f"mysql+pymysql://user:{'password'}@hostname:{sql_port}/{db}"
            # connect to mySQL server
            engine = create_engine(uri)

            with engine.connect() as conn:
                result = conn.execute(sql)

            # test insert statement
            sql = f"INSERT INTO {'2yr_bonds'} ({'Date'}, {'Rate'}) VALUES (curdate(), 1.0)"
            # execute statement, engine.execute() creates connection, executes, and then close()s itself
            engine.execute(sql)

        except Exception:
            print(traceback.format_exc())
            print(f"An SQL error has occurred.")
except Exception:
    print(traceback.format_exc())
    print("An SSH connection error occurred.")