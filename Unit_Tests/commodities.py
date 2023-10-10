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

    for row in data:
        print(row['symbol'])
        print(row['realtime_data']['price'])

    try:
        # create with context manager
        with connect.connect() as conn:
            for symbols in data:
                symbol = symbols['symbol']
                name = symbols['name']
                print(f"symbol: {symbol}\n name: {name}")
                # execute plain sql insert statement - transaction begins
                conn.execute(text(f"insert into `Commodity_List` values (NULL, {name}, {symbol})"))
            # end transaction
            conn.commit()
            # execute select statement, fetch cursorresult object
            result = conn.execute(text("select * from `Commodity_List`"))
            for row in result:
                print(row)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print("SQL connection error")

if __name__ == "__main__":
    main()
