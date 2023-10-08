# https://docs.sqlalchemy.org/en/20/changelog/migration_20.html


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

# common sqlalchemy exceptions
from sqlalchemy.exc import (
    SQLAlchemyError,
    DataError,
    DatabaseError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
    TimeoutError,
)

"""
csv code

with open('bonds.csv', mode='w') as output:
    csv_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in result:
        csv_writer.writerow([row.Date, row.BondDuration, row.Rate])
    output.flush()
"""

def load_json(path):
    print("Loading JSON...")
    with open(path) as file:
        data = json.load(file)
    
    return data

"""
connection function, creates engine and returns connection object
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
        # connect, must be closed
        connection = engine.connect()

        yield connection
    finally:
        connection.close()

def main():
    try:
        # maybe this will still close it
        with connect() as conn:

            conn.execute(text(f"insert into `Bonds` values (SYSDATE, 1.0, 2.0)"))
            conn.commit()
            print(f"Selecting values from database...")
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