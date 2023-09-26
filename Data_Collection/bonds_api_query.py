# Get data from the bonds API list file
# Parse the json so we know what our URL and keys are
# Iterate through the stocks using the key and url, then move onto the next API
import json


def load_config():
    config_file = open("Bonds_List.json", "r")
    config = json.load(config_file)
    return config

# def make_queries():
#     for api in len()

# code to only be executed if ran as script
if __name__ == "__main__":
    JSON_config = load_config()
    print(JSON_config[0]['date_windows'])
