# Get data from company info API list file
import json
import time
import os
import errno
import requests


# Load config file
def load_config():
    config_path = "Config/Company_Info_List.json"
    try:
        config_file = open(config_path, "r")
        config = json.load(config_file)
        return config
    except IOError:
        print(f"IOError while accessing historical query config file at path: {config_path}")


# Create API queries
def make_queries(parsed_api_url, parsed_api_key, query_list, api_rate_limit):
    output = []
    # Iterate through each stock and make an API call
    for query_itr in range(len(query_list)):
        query = query_list[query_itr]
        # Replace the URL parameters with our current API configs
        query = parsed_api_url.replace("{QUERY_PARAMS}", query).replace("{API_KEY}", parsed_api_key)
        response = requests.get(query)
        # Convert the response to json and append to list
        data = response.json()
        output += data
        if api_rate_limit is not None:
            time.sleep(60 / api_rate_limit)

    return output


# Write output file
def write_files(company_json):
    output_dir = "Output/"
    if not os.path.exists(os.path.dirname(output_dir)):
        try:
            os.makedirs(os.path.dirname(output_dir))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open("Output/Raw_Company_Info_Output.json", "w") as outfile:
        json.dump(company_json, outfile, indent=2)


# Code to only be executed if ran as script
if __name__ == "__main__":
    JSON_config = load_config()
    company_output = []

    # Iterate through each API in the list
    for api in range(len(JSON_config)):
        api_url = JSON_config[api]['url']
        api_key = JSON_config[api]['api_key']
        api_rate_limit = JSON_config[api]['rate_limit_per_min']
        company_list = JSON_config[api]['stocks']

        company_output = make_queries(api_url, api_key, company_list, api_rate_limit)

    write_files(company_output)
