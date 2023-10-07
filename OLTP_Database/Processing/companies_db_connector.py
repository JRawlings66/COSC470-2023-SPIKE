"""
- This script is used to take stock data collected from the Financial Modeling Prep API, and load it into the OLTP database.
- Data is read from a JSON output file, validated, then inserted into the database.
"""

import mysql.connector
import json
import datetime


def read_config(filename):
    try:
        with open(filename, "r") as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        print(f"Config file '{filename}' not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error decoding JSON in '{filename}'")
        exit(1)


# Load database credentials from the config file
config = read_config("config.json")


def read_output(filename):
    try:
        with open(filename, "r") as output_file:
            config = json.load(output_file)
        return config
    except FileNotFoundError:
        print(f"Output file '{filename}' not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error decoding JSON in '{filename}'")
        exit(1)


stock_data = read_output("../../Data_Collection/Output/Stocks_Output.json")

try:
    # Establish a connection to server
    connection = mysql.connector.connect(**config["companies"])

    if connection.is_connected():
        # Print the MySQL server version
        db_info = connection.get_server_info()
        print(f"Connected to MySQL Server version {db_info}")

        cursor = connection.cursor(buffered=True)

        # Iterate over stock data
        for stock in stock_data:
            # Variable Declarations
            symbol = stock["symbol"]
            company_name = stock["name"]
            open_price = stock["open"]
            high_price = stock["dayHigh"]
            low_price = stock["dayLow"]
            close_price = stock["price"]
            volume = stock["volume"]
            exchange = stock["exchange"]
            date = datetime.datetime.fromtimestamp(
                stock["timestamp"]
            )  # Date translated from Unix timestamp to DATETIME format

            # Queries
            get_company_id = f"SELECT id FROM Companies WHERE CompanyName = '{company_name}' AND Symbol = '{symbol}'"
            companies_insert = f"INSERT INTO Companies (CompanyName, Symbol) VALUES ('{company_name}', '{symbol}')"

            # Query Companies table for matching symbol.
            cursor.execute(f"SELECT COUNT(*) FROM Companies WHERE symbol = '{symbol}'")
            result = cursor.fetchone()
            num_rows = result[0]

            # If no matching symbol is found, create new entry in Companies table
            if num_rows == 0:
                # companies_insert query will cause trigger to fire, generating a new companyID associated with the stock
                cursor.execute(companies_insert)
                connection.commit()
                # Query companies table for new generated ID
                cursor.execute(get_company_id)
                company_id = cursor.fetchone()[0]
                # Insert into stock_values table
                cursor.execute(
                    f"INSERT INTO Stock_Values VALUES ('{company_id}', '{date}','{open_price}', '{high_price}', '{low_price}', '{close_price}', '{volume}', '{exchange}')"
                )
                connection.commit()
            # If matching symbol, insert into stocks_values using retrieved ID
            elif num_rows == 1:
                cursor.execute(get_company_id)
                company_id = cursor.fetchone()[0]
                cursor.execute(
                    f"INSERT INTO Stock_Values VALUES ('{company_id}', '{date}','{open_price}', '{high_price}', '{low_price}', '{close_price}', '{volume}', '{exchange}')"
                )
                connection.commit()

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if connection.is_connected():
        # Close the database connection
        connection.close()
        print("Connection closed")
