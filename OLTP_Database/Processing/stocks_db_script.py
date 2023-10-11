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
    data = load('../../Data_Collection/Output/Unified_Stocks_Output.json')

    try:
        # create with context manager
        with connect.connect() as conn:
            for entry in data:
                symbol = entry['symbol']
                name = entry['name']
                # establish if it exists already
                result = conn.execute(text(f"select ID from `Companies` where Symbol = '{symbol}'"))
                row = result.one_or_none()
                if row is None:
                    # execute plain sql insert statement - transaction begins
                    conn.execute(text(f"insert into `Companies`(`ID`, `CompanyName`, `Symbol`) values (NULL, '{name}', '{symbol}')"))
                    conn.commit()
                    # get the generated ID
                    result = conn.execute(text(f"select ID from `Companies` where Symbol = '{symbol}'")) 
                    CompanyID = result.one()[0]
                else:
                    CompanyID = row[0]
                    
                date = datetime.datetime.fromtimestamp(entry['realtime_data']['timestamp']) 
                companyOpen = entry['realtime_data']['open']
                high = entry['realtime_data']['dayHigh']
                low = entry['realtime_data']['dayLow']
                #close = entry['realtime_data']['previousClose'] no close
                volume = entry['realtime_data']['volume']
                exchange = entry['realtime_data']['exchange']
                try:
                    conn.execute(text(f"insert into `Stock_Values`(`CompanyID`, `Date`, `Open`, `High`, `Low`, `Close`, `Volume`, `Exchange`) values ('{CompanyID}', '{date}', '{companyOpen}', '{high}', '{low}', null, '{volume}', '{exchange}')"))
                    conn.commit()
                except IntegrityError as e: # catch duplicate entry
                    volume = volume # do nothing
                
                for h_entry in entry['historical_data']:
                    date = h_entry['date']
                    companyOpen = h_entry['open']
                    high = h_entry['high']
                    low = h_entry['low']
                    close = h_entry['close']
                    volume = h_entry['volume']
                    try:
                        conn.execute(text(f"insert into `Stock_Values`(`CompanyID`, `Date`, `Open`, `High`, `Low`, `Close`, `Volume`, `Exchange`) values ('{CompanyID}', '{date}', '{companyOpen}', '{high}', '{low}', '{close}', '{volume}', '{exchange}')"))
                        conn.commit()
                    except IntegrityError as e: # catch duplicate entries
                        continue
                
            
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print("SQL connection error")

if __name__ == "__main__":
    main()
