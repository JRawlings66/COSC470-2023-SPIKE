from contextlib import contextmanager
import credentials as cred
import json

from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text

"""
connection function, creates engine and returns connection object
decorator allows use of the context manager to close the connection automatically
could also be a class, but we'll leave it as a function unless there needs to be enough data attached to it to justify it
"""

@contextmanager
def connect():
    try:
        print(f"Connecting to database...")
        sql_port = 3306
        # database uri - connector://user:pass@hostname:sql_port(3306 by default)/database
        uri = f"mysql+pymysql://{cred.db['user']}:{cred.db['pass']}@{cred.db['host']}:{sql_port}/{cred.db['database']}"
        # create engine
        # echo=True for sql feedback on every op
        engine = create_engine(uri)
        # connect, no need to close manually
        connection = engine.connect()
        # generator - like a return with iteration, allows function to continue from a previous state after a return
        yield connection
    finally:
        # block executed when closed by context manager, as the with statement is really just a try/finally block
        connection.close()

def main():
    try:
        # create with context manager
        with connect() as conn:
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
                else:
                    for j in i['historical_data']:
                        # insert the rest of the data into index_values table
                        conn.execute(text("insert into `Index_Values` values (DATE(), '" + indexID + "'," + j['open'] + "," + j['high'] + "," + j['low'] + "," + j['close'] + "," + j['volume'] + ")"))
                        conn.commit()
    except Exception as e:
        print(e)
        print("SQL connection error")

# protected entrypoint
if __name__ == "__main__":
    main()