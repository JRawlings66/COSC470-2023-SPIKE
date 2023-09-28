# https://docs.sqlalchemy.org/en/20/changelog/migration_20.html

import traceback
import sys
import os
# import credentials # ssh/db credentials in a separate file
from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text
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

    two_year = table("2yr_bonds", column("Date"), column("Rate"))

    with engine.connect() as conn:
        conn.execute(text("insert into table (2yr_bonds) values (sysdate())"))
        conn.commit()
        
    with engine.connect() as conn:
        result = conn.execute(select(two_year))

    print(result.fetchall())

except Exception:
    print(traceback.format_exc())
    print(f"An SQL error has occurred.")
