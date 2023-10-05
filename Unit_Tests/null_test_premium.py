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

sql_port = 3306

class NullTest(unittest.TestCase):
    
    def test_bonds(self):
        creds = credentials.databases['bonds']
        uri = f"mysql+pymysql://{creds['user']}:{creds['pass']}@{creds['host']}:{sql_port}/{creds['database']}"
        engine = create_engine(uri)
        with self.assertRaises(IntegrityError):
            with engine.connect() as conn:
                conn.execute(text("insert into `Bonds` values (null, null, null)"))
                conn.commit()
                
    def test_index_values(self):
        creds = credentials.databases['index']
        uri = f"mysql+pymysql://{creds['user']}:{creds['pass']}@{creds['host']}:{sql_port}/{creds['database']}"
        engine = create_engine(uri)
        with self.assertRaises(IntegrityError):
            with engine.connect() as conn:
                conn.execute(text("insert into `Index_Values` values (null, null, null, null, null, null, null)"))
                conn.commit()
                
    def test_indices(self):
        creds = credentials.databases['index']
        uri = f"mysql+pymysql://{creds['user']}:{creds['pass']}@{creds['host']}:{sql_port}/{creds['database']}"
        engine = create_engine(uri)
        with self.assertRaises(IntegrityError):
            with engine.connect() as conn:
                conn.execute(text("insert into `Indices` values (null, null, null)"))
                conn.commit()
                
    def test_index_values(self):
        creds = credentials.databases['companies']
        uri = f"mysql+pymysql://{creds['user']}:{creds['pass']}@{creds['host']}:{sql_port}/{creds['database']}"
        engine = create_engine(uri)
        with self.assertRaises(IntegrityError):
            with engine.connect() as conn:
                conn.execute(text("insert into `Changelogs` values (null, null, null, null, null, null, null, null)"))
                conn.commit()
                
    def test_companies(self):
        creds = credentials.databases['companies']
        uri = f"mysql+pymysql://{creds['user']}:{creds['pass']}@{creds['host']}:{sql_port}/{creds['database']}"
        engine = create_engine(uri)
        with self.assertRaises(IntegrityError):
            with engine.connect() as conn:
                conn.execute(text("insert into `Companies` values (null, null, null)"))
                conn.commit()            
                
    def test_stock_values(self):
        creds = credentials.databases['companies']
        uri = f"mysql+pymysql://{creds['user']}:{creds['pass']}@{creds['host']}:{sql_port}/{creds['database']}"
        engine = create_engine(uri)
        with self.assertRaises(IntegrityError):
            with engine.connect() as conn:
                conn.execute(text("insert into `Stock_Values` values (null, null, null, null, null, null, null, null)"))
                conn.commit()                        
                
    def test_company_statements(self):
        creds = credentials.databases['companies']
        uri = f"mysql+pymysql://{creds['user']}:{creds['pass']}@{creds['host']}:{sql_port}/{creds['database']}"
        engine = create_engine(uri)
        with self.assertRaises(IntegrityError):
            with engine.connect() as conn:
                conn.execute(text("insert into `Company_Statements` values (null, null, null, null, null, null, null, null, null, null, null, null, null, null)"))
                conn.commit()             
                
    def test_commodity_list(self):
        creds = credentials.databases['commodities']
        uri = f"mysql+pymysql://{creds['user']}:{creds['pass']}@{creds['host']}:{sql_port}/{creds['database']}"
        engine = create_engine(uri)
        with self.assertRaises(IntegrityError):
            with engine.connect() as conn:
                conn.execute(text("insert into `Commodity_List` values (null, null, null)"))
                conn.commit()            
                
    def test_commodity_values(self):
        creds = credentials.databases['commodities']
        uri = f"mysql+pymysql://{creds['user']}:{creds['pass']}@{creds['host']}:{sql_port}/{creds['database']}"
        engine = create_engine(uri)
        with self.assertRaises(IntegrityError):
            with engine.connect() as conn:
                conn.execute(text("insert into `Commodity_Values` values (null, null, null, null, null, null, null)"))
                conn.commit()            

    #print(f"Test failed, null values inserted.")
    #print(f"Null values not inserted. Test successful.")
    
if __name__ == '__main__':
    unittest.main(verbosity=2)
