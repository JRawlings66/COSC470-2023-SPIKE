import datetime
import connect
import json
import traceback

from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

def load(path):
    with open(path) as file:
        data = json.load(file)
    return data

def main():
    # load json
    data = load('../../Data_Collection/Output/Unified_Index_Output.json')

    try:
        # create with context manager
        with connect.connect() as conn:
             for symbols in data:
                symbol = symbols['symbol']
                name = symbols['name']
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
                date = datetime.datetime.fromtimestamp(symbols['realtime_data']["timestamp"])
                indexOpen = symbols['realtime_data']['open']
                high = symbols['realtime_data']['high']
                low = symbols['realtime_data']['low']
                #close = symbols['realtime_data']['close']
                volume = symbols['realtime_data']['volume']
                try:
                    conn.execute(text(f"insert into `Index_Values`(`IndexID`, `Date`, `Open`, `High`, `Low`, `Close`, `Volume`) values ('{IndexID}', '{date}', '{indexOpen}', '{high}', '{low}', null, '{volume}')"))
                    conn.commit()           
                except IntegrityError as e:
                    volume = volume # do nothing  

                # process historical data
                for entry in symbols['historical_data']:
                    date = entry['date']
                    indexOpen = entry['open']
                    high = entry['high']
                    low = entry['low']
                    close = entry['close']
                    volume = entry['volume']
                    try: 
                        conn.execute(text(f"insert into `Index_Values`(`IndexID`, `Date`, `Open`, `High`, `Low`, `Close`, `Volume`) values ('{IndexID}', '{date}', '{indexOpen}', '{high}', '{low}', '{close}', '{volume}')"))
                        conn.commit()
                    except IntegrityError as e: # catch duplicate entries
                        continue
                
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print("SQL connection error")

# protected entrypoint
if __name__ == "__main__":
    main()