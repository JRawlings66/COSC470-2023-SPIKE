# https://docs.sqlalchemy.org/en/20/changelog/migration_20.html

import traceback
import sys
import os

from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text

class TestException(Exception):
    def __init__(self, problems):
        message = "Primary key violation for the following rows:\n"
        for problem in problems:
            message += f"  {problem}\n"
        super().__init__(message)

# 4 databases
db = ""
sql_port = 3306

try:
    print("Connecting to database...")
    uri = f"mysql+pymysql://user:{'password'}@hostname:{sql_port}/{db}"
    # connect to mySQL server
    engine = create_engine(uri)

    two_year = table("2yr_bonds", column("Date"), column("Rate"))

    #with engine.connect() as conn:
        #conn.execute(text("insert into `2yr_bonds` values (sysdate(), 1.0)"))
        #conn.commit()

    with engine.connect() as conn:
        print(f"Inserting null values into {db}.2yr_bonds...")
        conn.execute(text("insert into `2yr_bonds` values (null, null)"))
        conn.commit()

    #with engine.connect() as conn:
        #result = conn.execute(select(two_year))

    #print(result.fetchall())
    print(f"Test failed, null values inserted.")

except Exception:
    #print(traceback.format_exc())
    print(f"Null values not inserted. Test successful.")
