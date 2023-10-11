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
    data = load('../../Data_Collection/Output/Unified_Commodities_Output.json')

    try:
        # create with context manager
        with connect.connect() as conn:
            for symbols in data:
                symbol = symbols['symbol']
                name = symbols['name']
                # establish if it exists already
                result = conn.execute(text(f"select ID from `Commodity_List` where Symbol = '{symbol}'"))
                CommodityID = result.one_or_none()[0]
                if CommodityID is None:
                    # execute plain sql insert statement - transaction begins
                    conn.execute(text(f"insert into `Commodity_List`(`ID`, `Name`, `Symbol`) values (NULL, '{name}', '{symbol}')"))
                    conn.commit()
                    # get the generated ID
                    result = conn.execute(text(f"select ID from `Commodity_List` where Symbol = '{symbol}'")) 
                    CommodityID = result.one()[0]
                    
                date = datetime.datetime.fromtimestamp(symbols['realtime_data']['timestamp']) 
                commodityOpen = symbols['realtime_data']['open']
                high = symbols['realtime_data']['dayHigh']
                low = symbols['realtime_data']['dayLow']
                #close = symbols['realtime_data']['previousClose'] no close
                volume = symbols['realtime_data']['volume']
                try:
                    conn.execute(text(f"insert into `Commodity_Values`(`CommodityID`, `Date`, `Open`, `High`, `Low`, `Close`, `Volume`) values ('{CommodityID}', '{date}', '{commodityOpen}', '{high}', '{low}', null, '{volume}')"))
                except IntegrityError as e: # catch duplicate entry
                    #do nothing
                for entry in symbols['historical_data']:
                    date = entry['date']
                    commodityOpen = entry['open']
                    high = entry['high']
                    low = entry['low']
                    close = entry['close']
                    volume = entry['volume']
                    conn.execute(text(f"insert into `Commodity_Values`(`CommodityID`, `Date`, `Open`, `High`, `Low`, `Close`, `Volume`) values ('{CommodityID}', '{date}', '{commodityOpen}', '{high}', '{low}', '{close}', '{volume}')"))
                    try:
                        conn.commit()
                    except IntegrityError as e: # catch duplicate entries
                        continue
                
            
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print("SQL connection error")

if __name__ == "__main__":
    main()
