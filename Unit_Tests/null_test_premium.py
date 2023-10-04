# https://docs.sqlalchemy.org/en/20/changelog/migration_20.html

import traceback
import sys
import os
import unittest

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

db = ""
sql_port = 3306
uri = f"mysql+pymysql://user:{'password'}@hostname:{sql_port}/{db}"
# connect to mySQL server
engine = create_engine(uri)

class NullTest(unittest.TestCase):
    
    def test_2yr(self):
        with self.assertRaises(IntegrityError):
            with engine.connect() as conn:
                conn.execute(text("insert into `2yr_bonds` values (null, null)"))
                conn.commit()
                
    def test_5yr(self):
        with self.assertRaises(IntegrityError):
            with engine.connect() as conn:
                conn.execute(text("insert into `5yr_bonds` values (null, null)"))
                conn.commit()
    
    def test_7yr(self):
        with self.assertRaises(IntegrityError):
            with engine.connect() as conn:
                conn.execute(text("insert into `7yr_bonds` values (null, null)"))
                conn.commit()


    #print(f"Test failed, null values inserted.")
    #print(f"Null values not inserted. Test successful.")
    
if __name__ == '__main__':
    unittest.main(verbosity=2)
