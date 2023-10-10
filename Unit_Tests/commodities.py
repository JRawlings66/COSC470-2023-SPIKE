import connect
import json
import traceback

from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text
from sqlalchemy import insert


def load(path):
    with open(path) as file:
        data = json.load(file)
    return data


def main():
    # load json
    data = load('big_test.json')

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
                #unknown if we want realtime data included
                #commodityOpen = symbols.realtime_data['open']
                #commodity...
                #conn.execute(text(f"insert into `Commodity_Values`(`CommodityID`, `Date`, `Open`, `High`, `Low`, `Close`, `Volume`) values ('{CommodityID}', CURDATE, '{symbols[}')"))
                for entry in symbols['historical_data']:
                    date = entry['date']
                    commodityOpen = entry['open']
                    high = entry['high']
                    low = entry['low']
                    close = entry['close']
                    volume = entry['volume']
                    conn.execute(f"insert into `Commodity_Values`(`CommodityID`, `Date`, `Open`, `High`, `Low`, `Close`, `Volume`) values ('{CommodityID}', '{date}', '{commodityOpen}', '{high}', '{low}', '{close}', '{volume}')")
                # end this symbol's transaction
                conn.commit()
                
            
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print("SQL connection error")

if __name__ == "__main__":
    main()
