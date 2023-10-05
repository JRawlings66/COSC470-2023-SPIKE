# https://docs.sqlalchemy.org/en/20/changelog/migration_20.html


import traceback
import csv
import sys
import json
import credentials

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

def load_json(path):
    with open(path) as file:
        data = json.load(file)
    
    return data

def main():
    # dbname
    db = 'bonds'
    # json path for test purposes
    path = './test.json'
    creds = credentials.databases['bonds']
    # default sql port, shared between all db servers
    sql_port = 3306

    try:
        print("Loading JSON...")
        # load json to python dict
        data = load_json(path)
        
        print(f"Connecting to {db}...")
        uri = f"mysql+pymysql://{creds['user']}:{creds['pass']}@{creds['host']}:{sql_port}/{creds['database']}"
        # connect to mySQL server
        engine = create_engine(uri) # echo=True for sql feedback on every op
        # start engine
        with engine.connect() as conn:
            print(f"Inserting values into {db}...")
            for record in data:
                conn.execute(text(f"insert into `Bonds` values ({record['Date']}, {record['BondDuration']}, {record['Rate']})"))
            conn.commit()
            print(f"Selecting values from {db}...")
            result = conn.execute(text("select * from `Bonds`"))
            for row in result:
                print(row)
    except Exception:
        traceback.format_exc()
        print("SQL connection error")

# protected entrypoint
if __name__ == "__main__":
    main()