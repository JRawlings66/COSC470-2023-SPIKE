printf "[INFO] Executing API Queries...\n"
cd ~/COSC470-2023-SPIKE/Data_Collection || exit

printf "[INFO] Fetching realtime data...\n"
python3 stock_index_commodity_api_query.py
if [ $? -eq 0 ]
then
  printf "[INFO] Realtime stocks, indexes, and commodities data successfully retrieved.\n"
else
  # Redirect stdout from printf command to stderr.
  printf "  [ERROR] Error in fetching realtime stocks, indexes and commodities data.\n" >&2
fi

printf "[INFO] Fetching bonds data...\n"
python3 bonds_api_query.py
if [ $? -eq 0 ]
then
  printf "[INFO] Bonds data successfully retrieved.\n"
else
  # Redirect stdout from printf command to stderr.
  printf "[ERROR] Error in fetching bonds data.\n" >&2
fi

printf "[INFO] Fetching company info...\n"
python3 company_info_api_query.py
if [ $? -eq 0 ]
then
  printf "[INFO] Company info data successfully retrieved.\n"
else
  # Redirect stdout from printf command to stderr.
  printf "[ERROR] Error in fetching company info data.\n" >&2
fi

printf "[INFO] Fetching historical data...\n"
python3 historical_index_commodity_api_query.py
if [ $? -eq 0 ]
then
  printf "[INFO] Historical stocks, indexes, and commodities successfully retrieved.\n"
else
  # Redirect stdout from printf command to stderr.
  printf "[ERROR] Error in fetching historical stocks, indexes and commodities.\n" >&2
fi

printf "[INFO] All data processes complete.\n"
printf "[INFO] Performing data unification...\n"
python3 data_unification_process.py
if [ $? -eq 0 ]
then
  printf "[INFO] Data unification completed.\n"
else
  # Redirect stdout from printf command to stderr.
  printf "[ERROR] Error in data unification.\n" >&2
fi

printf "\n[INFO] Beginning OLTP DB insertions.\n"
cd ~/COSC470-2023-SPIKE/OLTP_Database/Processing || exit

printf "[INFO] Performing data insert on bonds DB...\n"
python3 bonds_db_script.py
if [ $? -eq 0 ]
then
  printf "[INFO] Data insertion completed.\n"
else
  # Redirect stdout from printf command to stderr.
  printf "[ERROR] Error in data insertion.\n" >&2
fi

printf "[INFO] Performing data insert on commodities DB...\n"
python3 commodities_db_script.py
if [ $? -eq 0 ]
then
  printf "[INFO] Data insertion completed.\n"
else
  # Redirect stdout from printf command to stderr.
  printf "[ERROR] Error in data insertion.\n" >&2
fi

printf "[INFO] Performing data insert on index DB...\n"
python3 index_db_script.py
if [ $? -eq 0 ]
then
  printf "[INFO] Data insertion completed.\n"
else
  # Redirect stdout from printf command to stderr.
  printf "[ERROR] Error in data insertion.\n" >&2
fi

printf "[INFO] Performing data insert on stocks DB...\n"
python3 stocks_db_script.py
if [ $? -eq 0 ]
then
  printf "[INFO] Data insertion completed.\n"
else
  # Redirect stdout from printf command to stderr.
  printf "[ERROR] Error in data insertion.\n" >&2
fi

printf "\n[INFO] All data insertions completed. Have a nice day!\n"

mysql --host="" --user="" --password="" <db_name>