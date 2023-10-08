import json
import datetime
import credentials as cred

from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text

## Load JSON output from Data Collection for Symbol Change Query
def read_output(filename):
    try:
        with open(filename, "r") as change_file:
            changes = json.load(change_file)
        return changes
    except FileNotFoundError:
        print(f"Output file '{filename}' not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error decoding JSON in '{filename}'.")
        exit(1)

company_change_list = read_output(f"../../Data_Collection/Output/'{replaceMe}'.json")

## Establish Connection with Database
@contextmanager
def connect():
    try:
        print(f"Connecting to database...")
        sql_port = 3306
        uri = f"mysql+pymysql://{cred.db['user']}:{cred.db['pass']}@{cred.db['host']}:{sql_port}/{cred.db['database']}"
        engine = create_engine(uri)
        connection = engine.connect()
        yield connection
    finally:
        connection.close()
        print("Database connection closed.")

## Main Functions of Process
def main():
    try:
        with connect() as db_conn:
            for change in company_change_list
    except Exception as e:
        print("Encountered SQL or system exception:")
        print(e)
        

if __name__ == ")__main__":
    main()