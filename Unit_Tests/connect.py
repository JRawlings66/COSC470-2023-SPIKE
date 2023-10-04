# https://docs.sqlalchemy.org/en/20/changelog/migration_20.html


import traceback
import csv
import pandas as pd
import credentials

from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text

# common sqlalchemy exceptions
from sqlalchemy.exc import (
    SQLAlchemyError,
    DataError,
    DatabaseError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
    TimeoutError,
)

# dummy custom exception for later
class TestException(Exception):
    def __init__(self, problems):
        message = "Primary key violation for the following rows:\n"
        for problem in problems:
            message += f"  {problem}\n"
        super().__init__(message)

def main():
    # db name
    db = ""
    # default sql port, shared between all db servers
    sql_port = 3306
    # set pandas options
    pd.set_option("display.max_rows", 100)
    pd.set_option("display.max_columns", None)
    
    # TODO; load csv from connection team, or convert json?
    """
    data = pd.read_csv("path/to/csv") # skiprows=
    # NaN to empty strings (or output csv will be filled with NaN's in empty fields)
    data = data.fillna('')
    """

    try:
        print(f"Connecting to {db}...")
        uri = f"mysql+pymysql://user:{'password'}@hostname:{sql_port}/{db}"
        # connect to mySQL server
        engine = create_engine(uri, echo=True)
        # create SQLAlchemy table object
        two_year = table("2yr_bonds", column("Date"), column("Rate"))

        # start mySQL engine
        with engine.connect() as conn:
            # select records from table TODO; select entire db
            # records = conn.execute(select(two_year))
            # read from sql into pandas dataframe object
            records = pd.read_sql(
                sql=two_year, #SQLAlchemy Selectable (select or text object)
                con=conn, # sqlalchemy engine connection
                )
            try:
                records.to_csv(
                    path_or_buf='bonds_db.csv', # output path
                    header=True, # write column headers
                    index=False, # don't write pandas index
                    mode='w', # truncate existing file, a for append, x for exclusive creation
                    )
            except Exception:
                traceback.format_exc()
                print("CSV error")
    except Exception:
        traceback.format_exc()
        print(f"SQL connection error")

# protected entrypoint
if __name__ == "__main__":
    main()