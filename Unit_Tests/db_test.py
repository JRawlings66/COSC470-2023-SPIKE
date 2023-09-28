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
sql_port = 3306

try:
    print("Connecting to database...")
    uri = f"mysql+pymysql://db5014580903.hosting-data.io:{'COSC-470-admin'}@127.0.0.1:{sql_port}/{db}"
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
