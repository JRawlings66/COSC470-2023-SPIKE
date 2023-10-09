import json
import time
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
        sys.stderr.write(
            f"IOError while accessing raw realtime stock data file at path: {file_path}.\nThis could because the file "
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

                # Find the corresponding real-time data entry based on the symbol
                real_time_entry = None
                for entry in raw_realtime_json:
                    if entry["symbol"] == symbol:
                        real_time_entry = entry
                        break

                # dictionary for historical data
                historical_combined = {
                    "symbol": symbol,
                    "name": real_time_entry["name"] if real_time_entry else "",  # None types prevention
                    "realtime_data": real_time_entry if real_time_entry else {},  # Empty entry prevention
                    "historical_data": historical_entry["historical"],
                }

                # Append the combined entry to the list
                combined_data.append(historical_combined)
            except KeyError:
                print("Empty entry for historical data, skipping...")
                continue
    except TypeError:
        pass
    # Iterate through the real-time data
    try:
        for real_time_entry in raw_realtime_json:
            try:
                symbol = real_time_entry["symbol"]

                # Check if there is already a combined entry for this symbol
                existing_entry = None
                for entry in combined_data:
                    if entry["symbol"] == symbol:
                        existing_entry = entry
                        break

                if not existing_entry:
                    # If there's no existing entry, create a new one with real-time data
                    combined_entry = {
                        "symbol": symbol,
                        "name": real_time_entry["name"],
                        "realtime_data": real_time_entry,
                        "historical_data": {},
                    }
                    combined_data.append(combined_entry)
            except KeyError:
                print("Empty entry for real time data, skipping...")
                continue
    except TypeError:
        pass

    return combined_data


if __name__ == "__main__":
    # Load the files into JSON
    realtime_stocks_json = load_files("Output/Raw_Stocks_Output.json")
    realtime_commodity_json = load_files("Output/Raw_Commodity_Output.json")
    realtime_index_json = load_files("Output/Raw_Index_Output.json")

    historical_stocks_json = load_files("Output/Raw_Historical_Stocks_Output.json")
    historical_commodity_json = load_files("Output/Raw_Historical_Index_Output.json")
    historical_index_json = load_files("Output/Raw_Historical_Index_Output.json")

    # Call to unify files.
    unified_stocks_json = unify_realtime_historical(realtime_stocks_json, historical_stocks_json)
    unified_commodities_json = unify_realtime_historical(realtime_commodity_json, historical_commodity_json)
    unified_index_json = unify_realtime_historical(realtime_index_json, historical_index_json)

    # Output files.
    write_files(unified_stocks_json, "Output/Unified_Stocks_Output.json")
    write_files(unified_commodities_json, "Output/Unified_Commodities_Output.json")
    write_files(unified_index_json, "Output/Unified_Index_Output.json")
