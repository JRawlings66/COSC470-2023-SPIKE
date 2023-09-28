import traceback
import sys
import os
# import credentials # ssh/db credentials in a separate file
from sqlalchemy import create_engine, sql
# from sshtunnel import SSHTunnelForwarder
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
    uri = f"mysql+pymysql://dbu362865:{'cosc-470-admin'}@db5014580903.hosting-data.io:{sql_port}/{db}"
    # connect to mySQL server
    engine = create_engine(uri)

    # test insert statement
    stmt = sql.text(f"INSERT INTO `2yr_bonds` VALUES (sysdate(), 1.0);")

    with engine.connect() as conn:
        result = conn.execute(stmt)

except Exception:
    print(traceback.format_exc())
    print(f"An SQL error has occurred.")
