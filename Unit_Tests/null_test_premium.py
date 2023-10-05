# https://docs.sqlalchemy.org/en/20/changelog/migration_20.html

import traceback
import sys
import os
import credentials
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

db = "bonds"
sql_port = 3306
# load database credentials dict
creds = credentials.databases[db]
uri = f"mysql+pymysql://{creds['user']}:{creds['pass']}@{creds['host']}:{sql_port}/{creds['database']}"
# connect to mySQL server
engine = create_engine(uri)

class NullTest(unittest.TestCase):
    
    def test_bonds(self):
        with self.assertRaises(IntegrityError):
            with engine.connect() as conn:
                conn.execute(text("insert into `Bonds` values (null, null, null)"))
                conn.commit()


    #print(f"Test failed, null values inserted.")
    #print(f"Null values not inserted. Test successful.")
    
if __name__ == '__main__':
    unittest.main(verbosity=2)
