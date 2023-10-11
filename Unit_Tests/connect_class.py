import credentials as cred

from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text

"""
class may be more prudent, as with the function we create a new engine for every 'with' statement call. a class
allows us to access the engine directly as well, for creating Table objects
"""
class connect:
    def __init__(self):
        self.sql_port = 3306
        self.uri = f"mysql+pymysql://{cred.db['user']}:{cred.db['pass']}@{cred.db['host']}:{sql_port}/{cred.db['database']}"
        self.engine = create_engine(self.uri, echo=False)
        self.connection = None
    # runs when the with statement is entered
    def __enter__(self):
        self.connection = self.engine.connect()
        return self
    # runs when the with statement is exited
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

def main():
    try:
        # create with context manager
        with connect() as conn:
            # execute plain sql insert statement - transaction begins
            conn.execute(text("insert into `Bonds` values (DATE(), 1.0, 2.0)"))
            # end transaction
            conn.commit()
            # execute select statement, fetch cursorresult object
            result = conn.execute(text("select * from `Bonds`"))
            for row in result:
                print(row.Rate)
    except Exception as e:
        print(e)
        print("SQL connection error")

# protected entrypoint
if __name__ == "__main__":
    main()