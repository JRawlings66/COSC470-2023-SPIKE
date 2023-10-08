import traceback
import csv
import sys
import json
from contextlib import contextmanager
import credentials as cred

from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text

"""
connection function, creates engine and returns connection object
decorator allows use of the context manager to close the connection automatically
could also be a class, but we'll leave it as a function unless there needs to be enough data attached to it to justify it
"""
@contextmanager
def connect():
    try:
        print(f"Connecting to database...")
        sql_port = 3306
        # database uri
        uri = f"mysql+pymysql://{cred.db['user']}:{cred.db['pass']}@{cred.db['host']}:{sql_port}/{cred.db['database']}"
        # create engine
        # echo=True for sql feedback on every op
        engine = create_engine(uri)
        # connect, no need to close manually
        connection = engine.connect()
        # generator - like a return with iteration, allows function to continue from a previous state after a return
        yield connection
    finally:
        # block executed when closed by context manager, as the with statement is really just a try/finally block
        connection.close()

def main():
    try:
        # create with context manager
        with connect() as conn:
            # execute plain sql insert statement
            conn.execute(text("insert into `Bonds` values (DATE(), 1.0, 2.0)"))
            conn.commit()
            # execute select statement, fetch cursorresult object
            result = conn.execute(text("select * from `Bonds`"))
            for row in result:
                print(row.Rate)
    except Exception as e:
        print(e)
        traceback.format_exc()
        print("SQL connection error")

# protected entrypoint
if __name__ == "__main__":
    main()