# Data Collection Folder
- Contains process scripts for API and data collection
- Contains configurable lists for API source and Website Information

# Configuration:
* /Config/Bonds_List.json is the configuration file for which dates we want frm the US treasury.
* Stock_IndexComp_Comm_List.json is the configuration file for which stocks, index composites and
commodities we wish to fetch from each API.
# Processes:
* bonds_api_query.py is the script to fetch said bonds.
* stock_index_commodity_api_query.py is the script to fetch said data.
# File outputs:
* /Output/Bonds_Output.json
* /Output/Commodity_Output.json
* /Output/Index_Output.json
* /Output/Stocks_Output.json

Running these two processes will yield examples of data. The Data is not yet unified.

https://lucid.app/documents/view/d1e3a627-4c66-4bf7-a959-17de0c152870
