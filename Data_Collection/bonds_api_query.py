# Get data from the bonds API list file
# Parse the json so we know what our URL and keys are
# Iterate through the stocks using the key and url, then move onto the next API
# TODO make the directories for file read and out absolute ie not relative locations to the script
import json
import time
import os
import errno
import requests


# Loads the configuration file.
def load_config():
    config_file = open("Config/Bonds_List.json", "r")
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
        api_rate_limit = JSON_config[api]['rate_limit_per_min']

        # Iterate through each start-end date pair and make a API call
        for date in range(len(api_datewindows)):
            start_date = api_datewindows[date][0]
            end_date = api_datewindows[date][1]
            # Replace the URL parameters with our current API configs
            query = api_url.replace("{START_DATE}", start_date).replace("{END_DATE}", end_date).replace("{API_KEY}",
                                                                                                        api_key)
            response = requests.get(query)
            # convert the response to json and append to list
            data = response.json()
            bonds_output += data

            # Rate limit the query speed based on the rate limit
            # From inside the JSON. Check that the key wasnt valued at null, signifying no rate limit.
            if api_rate_limit is not None:
                time.sleep(60/api_rate_limit)

    return bonds_output


def write_file(output):
    output_dir = "Output/"
    if not os.path.exists(os.path.dirname(output_dir)):
        try:
            os.makedirs(os.path.dirname(output_dir))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open("Output/Raw_Bonds_Output.json", "w") as outfile:
        json.dump(output, outfile, indent=4)


# code to only be executed if ran as script
if __name__ == "__main__":
    JSON_config = load_config()
    output = make_queries()
    write_file(output)
