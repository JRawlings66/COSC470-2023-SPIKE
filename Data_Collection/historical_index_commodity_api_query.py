# Get historical data from the bonds API list file
# Parse the json so we know what our URL and keys are
# Iterate through the stocks using the key and url, then move onto the next API
# TODO make the directories for file read and out absolute ie not relative locations to the script
import json
import time
import os
import errno
import requests
import datetime


# Loads the configuration file.
def load_config():
    config_path = "Config/Historical_Stock_IndexComp_Comm_List.json"
    try:
        config_file = open(config_path, "r")
        config = json.load(config_file)
        return config
    except IOError:
        print(f"IOError while accessing historical query config file at path: {config_path}")


def make_queries(parsed_api_url, parsed_api_key, query_list, api_rate_limit, observable_days):
    output = []
    # Get today's date and format yyyy-mm-dd so it matches query params
    today = datetime.date.today()
    today_formatted = today.strftime("%Y-%m-%d")

    # Get the date from observable_days key and format to match query params
    days_prior = datetime.timedelta(days=observable_days)
    date_prior = today - days_prior
    date_prior_formatted = date_prior.strftime("%Y-%m-%d")

    # Iterate through each stocks and make a API call
    # TODO make it query with 5 items at a time ("APPL, TSLA, %5EGSPC")
    for query_itr in range(len(query_list)):
        query = query_list[query_itr]
        # Replace the URL parameters with our current API configs
        query = parsed_api_url.replace("{QUERY_PARAMS}", query).replace("{API_KEY}", parsed_api_key).replace(
            "{FROM_DATE}", date_prior_formatted).replace("{TODAY_DATE}", today_formatted)
        response = requests.get(query)
        # convert the response to json and append to list
        data = response.json()
        output.append(data)
        # print(output)
        # Rate limit the query speed based on the rate limit
        # From inside the JSON. Check that the key wasnt valued at null, signifying no rate limit.
        if api_rate_limit is not None:
            time.sleep(60 / api_rate_limit)

    return output


def write_files(stock_json, index_json, commodity_json):
    output_dir = "Output/"
    if not os.path.exists(os.path.dirname(output_dir)):
        try:
            os.makedirs(os.path.dirname(output_dir))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open("Output/Raw_Historical_Stocks_Output.json", "w") as outfile:
        json.dump(stock_json, outfile, indent=4)

    with open("Output/Raw_Historical_Index_Output.json", "w") as outfile:
        json.dump(index_json, outfile, indent=4)

    with open("Output/Raw_Historical_Commodity_Output.json", "w") as outfile:
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
        api_rate_limit = JSON_config[api]['rate_limit_per_min']
        api_observable_days = JSON_config[api]['observable_days']
        stock_list = JSON_config[api]['stocks']
        index_list = JSON_config[api]['index_composites']
        commodity_list = JSON_config[api]['commodities']

        stock_output = make_queries(api_url, api_key, stock_list, api_rate_limit, api_observable_days)
        index_output = make_queries(api_url, api_key, index_list, api_rate_limit, api_observable_days)
        commodity_output = make_queries(api_url, api_key, commodity_list, api_rate_limit, api_observable_days)

    write_files(stock_output, index_output, commodity_output)
