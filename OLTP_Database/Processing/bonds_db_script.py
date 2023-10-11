import connect
import json
import traceback

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError


def load(path):
    try:
        with open(path, "r") as output_file:
            output_data = json.load(output_file)
        return output_data
    except FileNotFoundError:
        print(f"Output file '{path}' not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error decoding JSON in '{path}'")
        exit(1)

def main():
    # load json
    data = load('../../Data_Collection/Output/Raw_Bonds_Output.json')

    try:
        # create with context manager
        with connect.connect() as conn:
            for entry in data:
                date = entry['date']
                for row in entry:
                    # skip the first row
                    if row == "date":
                        continue
                    bondDuration = row
                    rate = entry[row]
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
