import datetime
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
    data = load('../../Data_Collection/Output/Unified_Index_Output.json')

    try:
        # create with context manager
        with connect.connect() as conn:
             for entry in data:
                symbol = entry['symbol']
                name = entry['name']
                # check if index exists in indices table
                result = conn.execute(text(f"select ID from `Indices` where Symbol = '{symbol}'"))
                row = result.one_or_none()
                if row is None:
                    # execute plain sql insert statement - transaction begins
                    conn.execute(text(f"insert into `Indices`(`ID`, `Name`, `Symbol`) values (NULL, '{name}', '{symbol}')"))
                    conn.commit()
                    # get the generated ID
                    result = conn.execute(text(f"select ID from `Indices` where Symbol = '{symbol}'")) 
                    IndexID = result.one()[0]
                else:
                    IndexID = row[0]
                # process realtime data
                date = datetime.datetime.fromtimestamp(entry['realtime_data']["timestamp"])
                indexOpen = entry['realtime_data']['open']
                high = entry['realtime_data']['dayHigh']
                low = entry['realtime_data']['dayLow']
                #close = entry['realtime_data']['close']
                volume = entry['realtime_data']['volume']
                try:
                    conn.execute(text(f"insert into `Index_Values`(`IndexID`, `Date`, `Open`, `High`, `Low`, `Close`, `Volume`) values ('{IndexID}', '{date}', '{indexOpen}', '{high}', '{low}', null, '{volume}')"))
                    conn.commit()           
                except IntegrityError as e:
                    volume = volume # do nothing  

                # process historical data
                for h_entry in entry['historical_data']:
                    date = h_entry['date']
                    indexOpen = h_entry['open']
                    high = h_entry['high']
                    low = h_entry['low']
                    close = h_entry['close']
                    volume = h_entry['volume']
                    try: 
                        conn.execute(text(f"insert into `Index_Values`(`IndexID`, `Date`, `Open`, `High`, `Low`, `Close`, `Volume`) values ('{IndexID}', '{date}', '{indexOpen}', '{high}', '{low}', '{close}', '{volume}')"))
                        conn.commit()
                    except IntegrityError as e: # catch duplicate entries
                        continue
                
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print("SQL connection error")

# protected h_entrypoint
if __name__ == "__main__":
    main()