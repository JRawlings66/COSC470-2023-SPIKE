# Get data from the bonds API list file
# Parse the json so we know what our URL and keys are
# Iterate through the stocks using the key and url, then move onto the next API
# TODO make the directories for file read and out absolute ie not relative locations to the script
import json
import requests

# Loads the configuration file.
def load_config():
    config_file = open("Bonds_List.json", "r")
    config = json.load(config_file)
    return config


def make_queries():
    bonds_output = []

    # Iterate through each API in the list
    for api in range(len(JSON_config)):
        # Get the parameters for the query, including the list of start end dates
        api_url = JSON_config[api]['api']
        api_key = JSON_config[api]['api_key']
        api_datewindows = JSON_config[api]['date_windows']

        # Iterate through each start-end date pair and make a API call
        # TODO Rate limit this, as it can get super crazy (100 calls/min is what were allowed)
        for date in range(len(api_datewindows)):
            start_date = api_datewindows[date][0]
            end_date = api_datewindows[date][1]
            # Replace the URL parameters with our current API configs
            query = api_url.replace("{START_DATE}", start_date).replace("{END_DATE}", end_date).replace("{API_KEY}",                                                                                    api_key)
            response = requests.get(query)
            # convert the response to json and append to list
            data = response.json()
            bonds_output += data
    return bonds_output


def write_file(output):
    with open("Bonds_Output.json", "w") as outfile:
        json.dump(output, outfile, indent=4)


# code to only be executed if ran as script
if __name__ == "__main__":
    JSON_config = load_config()
    output = make_queries()
    write_file(output)
