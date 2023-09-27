# Get data from the bonds API list file
# Parse the json so we know what our URL and keys are
# Iterate through the stocks using the key and url, then move onto the next API
# TODO make the directories for file read and out absolute ie not relative locations to the script
import json
import requests


# Loads the configuration file.
def load_config():
    config_file = open("Stock_IndexComp_Comm_List.json", "r")
    config = json.load(config_file)
    return config


def make_queries(parsed_api_url, parsed_api_key, query_list):
    output = []

    # Iterate through each stocks and make a API call
    # TODO Rate limit this, as it can get super crazy (100 calls/min is what were allowed)
    #   Make it query 5 at a time for instance
    for query_itr in range(len(query_list)):
        query = query_list[query_itr]
        # Replace the URL parameters with our current API configs
        query = parsed_api_url.replace("{QUERY_PARAMS}", query).replace("{API_KEY}", parsed_api_key)
        response = requests.get(query)
        # convert the response to json and append to list
        data = response.json()
        output += data
    return output


def write_files(stock_json, index_json, commodity_json):
    with open("Stocks_Output.json", "w") as outfile:
        json.dump(stock_json, outfile, indent=4)

    with open("Index_Output.json", "w") as outfile:
        json.dump(index_json, outfile, indent=4)

    with open("Commodity_Output.json", "w") as outfile:
        json.dump(commodity_json, outfile, indent=4)


# code to only be executed if ran as script
if __name__ == "__main__":
    JSON_config = load_config()
    stock_output = []
    index_output = []
    commodity_output = []

    # Iterate through each API in the list
    for api in range(len(JSON_config)):
        api_url = JSON_config[api]['url']
        api_key = JSON_config[api]['api_key']
        stock_list = JSON_config[api]['stocks']
        index_list = JSON_config[api]['index_composites']
        commodity_list = JSON_config[api]['commodities']

        stock_output = make_queries(api_url, api_key, stock_list)
        index_output = make_queries(api_url, api_key, index_list)
        commodity_output = make_queries(api_url, api_key, commodity_list)

    write_files(stock_output, index_output, commodity_output)
