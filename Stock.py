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


def make_queries():
    bonds_output = []

    # Iterate through each API in the list
    for api in range(len(JSON_config)):
        # Get the parameters for the query, including the list of start end dates
        api_url = JSON_config[api]['url']
        api_key = JSON_config[api]['api_key']
        api_stocks = JSON_config[api]['stocks']

        # Iterate through each stocks and make a API call
        # TODO Rate limit this, as it can get super crazy (100 calls/min is what were allowed)
        for stock in range(len(api_stocks)):
            stocks = api_stocks[stock]
            # Replace the URL parameters with our current API configs
            query = api_url.replace("{QUERY_PARAMS}", stocks).replace("{API_KEY}", api_key)
            response = requests.get(query)
            # convert the response to json and append to list
            data = response.json()
            bonds_output += data
    return bonds_output


def write_file(output):
    with open("stocks.json", "w") as outfile:
        json.dump(output, outfile, indent=4)


# code to only be executed if ran as script
if __name__ == "__main__":
    JSON_config = load_config()
    output = make_queries()
    write_file(output)