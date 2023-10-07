import json
import time
import os
import errno


def write_files(stock_json):
    output_dir = "Output/"
    if not os.path.exists(os.path.dirname(output_dir)):
        try:
            os.makedirs(os.path.dirname(output_dir))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open("Output/Unified_Historical_Stocks_Output.json", "w") as outfile:
        json.dump(stock_json, outfile, indent=4)


def load_files():
    raw_realtime_stock_path = "Output/Raw_Stocks_Output.json"
    try:
        raw_realtime_stock_file = open(raw_realtime_stock_path)
        raw_stocks_json = json.load(raw_realtime_stock_file)
    except IOError:
        print(f"IOError while accessing raw realtime stock data file at path: {raw_realtime_stock_path}")

def unify_files():


if __name__ == "__main__":
    raw_stocks_json = []
    print("hello")
