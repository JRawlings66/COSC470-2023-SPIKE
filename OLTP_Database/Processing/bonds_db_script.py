import connect
import json
import traceback
import datetime

from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError


def load(path):
    with open(path) as file:
        data = json.load(file)
    return data


def main():
    # load json
    data = load('../../Data_Collection/Output/Raw_Bonds_Output.json')

    try:
        # create with context manager
        with connect.connect() as conn:
            for entry in data:
                date = entry['date']
                for row in entry[1:]:
                    bondDuration = row[0]
                    rate = row[1]
                    try:
                        conn.execute(text(f"insert into `Bonds`(`Date`, `BondDuration`, `Rate`) values ('{date}', '{bondDuration}', '{rate}')"))
                        conn.commit()
                    except IntegrityError as e: # catch duplicate entries
                        continue
                
            
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print("SQL connection error")

if __name__ == "__main__":
    main()
