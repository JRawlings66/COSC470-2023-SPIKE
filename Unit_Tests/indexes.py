import connect
import json
import traceback

from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text

def main():
    try:
        # create with context manager
        with connect.connect() as conn:
            # reference index_output.json file, import into json object
             index = json.loads(index_output.json)
             for i in index:
                symbol = i['symbol']
                # check if index exists in indices table
                indexID = conn.execute(text("select ID from `Indices` where Symbol = '" + symbol + "')"))
                if not indexID:
                    # insert will create an auto incremented id
                    conn.execute(text("insert into `Indices` values ('" + symbol + "', '" + i['name'] + "')"))
                    conn.commit()
                    # after commit, we can then pull the auto inserted id
                    indexID = conn.execute(text("select ID from `Indices` where Symbol = '" + symbol + "'"))
                for j in i['historical_data']:
                    # insert the rest of the data into index_values table
                    conn.execute(text("insert into `Index_Values` values (DATE(), '" + indexID + "'," + j['open'] + "," + j['high'] + "," + j['low'] + "," + j['close'] + "," + j['volume'] + ")"))
                    conn.commit()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print("SQL connection error")

# protected entrypoint
if __name__ == "__main__":
    main()