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
            for change in company_change_list:
                old_symbol = change["oldSymbol"]
                new_symbol = change["newSymbol"]
                symbol_changed = 0
                if old_symbol != new_symbol:
                    symbol_changed = 1
                company_name = change["name"]
                result = db_conn.execute(text(f"SELECT * FROM `Companies` WHERE Symbol='{old_symbol}'"))
                if not result.first():
                    continue
                ## q_result = result.mappings() for dict with column-based keys?
                stored_company_name = result.row.CompanyName ## Please review this line for appropriate accessing of result attr
                company_id = result.row.ID ## Please review this line for appropriate accessing of result attr
                name_changed = 0
                if stored_company_name != company_name:
                    name_changed = 1
                date = datetime.now()
                db_conn.execute(text(f"INSERT INTO `Changelogs` VALUES('{company_id}','{date}','{new_symbol}','{old_symbol}','{symbol_changed}','{company_name}','{stored_company_name}','{name_changed}')"))
    except Exception as e:
        print("Encountered SQL or system exception:")
        print(e)
        

if __name__ == ")__main__":
    main()