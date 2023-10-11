import json
import os
import errno
import sys


def write_files(unified_json, output_path):
    output_dir = "Output/"  # This hsouldnt be static, but for now it'll be hardcoded.
    if not os.path.exists(os.path.dirname(output_dir)):
        try:
            os.makedirs(os.path.dirname(output_dir))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(output_path, "w") as outfile:
        json.dump(unified_json, outfile, indent=2)


def load_files(file_path):
    try:
        raw_json_file = open(file_path)
        return json.load(raw_json_file)
    except (IOError, ValueError) as error:
        print(
            f"IOError while accessing raw input data file at path: {file_path}.\n\tThis could because the file "
            f"is not found, or the JSON is not valid.")


def unify_realtime_historical(raw_realtime_json, raw_historical_json):
    # Create a dictionary to store the combined data
    combined_data = []

    # goofy way to get the files to not freak out and print even if one structure on a None type.
    if raw_realtime_json is None:
        raw_realtime_json = []

    if raw_historical_json is None:
        raw_historical_json = []

    # Iterate through the historical data
    try:
        for historical_entry in raw_historical_json:
            try:
                symbol = historical_entry["symbol"]

                # Remove the label field
                for day in range(len(historical_entry)):
                    try:
                        del (historical_entry['historical'][day]['label'])
                    except IndexError:
                        pass  # Sometimes on holidays, commodities will have an uneven amount of entries vs a stock

                # Find the corresponding real-time data entry based on the symbol
                real_time_entry = None
                for entry in raw_realtime_json:
                    if entry["symbol"] == symbol:
                        real_time_entry = entry
                        break

                # dictionary for historical data
                historical_combined = {
                    "symbol": symbol,
                    "name": real_time_entry["name"] if real_time_entry else get_company_name_from_config(symbol),
                    # None types prevention
                    "realtime_data": real_time_entry if real_time_entry else {},  # Empty entry prevention
                    "historical_data": historical_entry["historical"],
                }

                # Append the combined entry to the list
                combined_data.append(historical_combined)
            except KeyError:
                print("Empty entry for historical data, skipping...")
                continue
    except TypeError as error:
        print(error)
        pass
    # Iterate through the real-time data
    try:
        for real_time_entry in raw_realtime_json:
            try:
                symbol = real_time_entry["symbol"]
                name = real_time_entry["name"]

                # Check if there is already a combined entry for this symbol
                existing_entry = None
                for entry in combined_data:
                    if entry["symbol"] == symbol:
                        existing_entry = entry
                        break

                # Remove the symbol field
                for day in range(len(real_time_entry)):
                    if symbol in real_time_entry.keys():
                        del (real_time_entry['symbol'])
                    if name in real_time_entry.keys():
                        del (real_time_entry['name'])

                if not existing_entry:
                    # If there's no existing entry, create a new one with real-time data
                    combined_entry = {
                        "symbol": symbol,
                        "name": name,
                        "realtime_data": real_time_entry,
                        "historical_data": {},
                    }
                    combined_data.append(combined_entry)
            except KeyError as error:
                raise error
                print("Empty entry for real time data, skipping...")
                continue
    except TypeError as error:
        print(error)
        pass

    return combined_data


def get_company_name_from_config(symbol):
    """
    Searches the historical config file for the company name that matches
    the symbol. Used when no real time data is provided, and thus a name must be found.
    TODO: Fix the fact this is horribly optimized.
    :type symbol: str
    :param symbol: Company symbol
    :return: Company name (str)
    """

    config_path = "Config/Historical_Stock_IndexComp_Comm_List.json"

    try:
        config_file = open(config_path, "r")
        config = json.load(config_file)
        for api in range(len(config)):
            for stock in range(len(config[api]["stocks"])):
                if config[api]["stocks"][stock]["symbol"] == symbol:
                    # print(config[api]["stocks"][stock]["name"])
                    return config[api]["stocks"][stock]["name"]

            for index in range(len(config[api]["index_composites"])):
                if config[api]["index_composites"][index]["symbol"] == symbol:
                    # print(config[api]["index_composites"][index]["name"])
                    return config[api]["index_composites"][index]["name"]

            for commodity in range(len(config[api]["commodities"])):
                if config[api]["commodities"][commodity]["symbol"] == symbol:
                    # print(config[api]["commodities"][commodity]["name"])
                    return config[api]["commodities"][commodity]["name"]

    except IOError:
        print(f"IOError while accessing historical stock/index/commodity query config at path: {config_path}")


if __name__ == "__main__":
    # Load the files into JSON
    realtime_stocks_json = load_files("Output/Raw_Stocks_Output.json")
    realtime_commodity_json = load_files("Output/Raw_Commodity_Output.json")
    realtime_index_json = load_files("Output/Raw_Index_Output.json")

    historical_stocks_json = load_files("Output/Raw_Historical_Stocks_Output.json")
    historical_commodity_json = load_files("Output/Raw_Historical_Commodity_Output.json")
    historical_index_json = load_files("Output/Raw_Historical_Index_Output.json")

    # Call to unify files.
    unified_stocks_json = unify_realtime_historical(realtime_stocks_json, historical_stocks_json)
    unified_commodities_json = unify_realtime_historical(realtime_commodity_json, historical_commodity_json)
    unified_index_json = unify_realtime_historical(realtime_index_json, historical_index_json)

    # Output files.
    write_files(unified_stocks_json, "Output/Unified_Stocks_Output.json")
    write_files(unified_commodities_json, "Output/Unified_Commodities_Output.json")
    write_files(unified_index_json, "Output/Unified_Index_Output.json")
