import connect
import json
import traceback
import datetime

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
    data = load('../../Data_Collection/Output/Unified_Commodities_Output.json')

    try:
        # create with context manager
        with connect.connect() as conn:
            for entry in data:
                symbol = entry['symbol']
                name = entry['name']
                # establish if it exists already
                result = conn.execute(text(f"select ID from `Commodity_List` where Symbol = '{symbol}'"))
                row = result.one_or_none()
                if row is None:
                    # execute plain sql insert statement - transaction begins
                    conn.execute(text(f"insert into `Commodity_List`(`ID`, `Name`, `Symbol`) values (NULL, '{name}', '{symbol}')"))
                    conn.commit()
                    # get the generated ID
                    result = conn.execute(text(f"select ID from `Commodity_List` where Symbol = '{symbol}'")) 
                    CommodityID = result.one()[0]
                else:
                    CommodityID = row[0]
                    
                date = datetime.datetime.fromtimestamp(entry['realtime_data']['timestamp']) 
                commodityOpen = entry['realtime_data']['open']
                high = entry['realtime_data']['dayHigh']
                low = entry['realtime_data']['dayLow']
                #close = entry['realtime_data']['previousClose'] no close
                volume = entry['realtime_data']['volume']
                try:
                    conn.execute(text(f"insert into `Commodity_Values`(`CommodityID`, `Date`, `Open`, `High`, `Low`, `Close`, `Volume`) values ('{CommodityID}', '{date}', '{commodityOpen}', '{high}', '{low}', null, '{volume}')"))
                    conn.commit()
                except IntegrityError as e: # catch duplicate entry
                    volume = volume # do nothing
                
                for h_entry in entry['historical_data']:
                    date = h_entry['date']
                    commodityOpen = h_entry['open']
                    high = h_entry['high']
                    low = h_entry['low']
                    close = h_entry['close']
                    volume = h_entry['volume']
                    try:
                        conn.execute(text(f"insert into `Commodity_Values`(`CommodityID`, `Date`, `Open`, `High`, `Low`, `Close`, `Volume`) values ('{CommodityID}', '{date}', '{commodityOpen}', '{high}', '{low}', '{close}', '{volume}')"))
                        conn.commit()
                    except IntegrityError as e: # catch duplicate entries
                        continue
                
            
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print("SQL connection error")

if __name__ == "__main__":
    main()
