import pandas as pd
import json

def read_csv(file_path):
    #Reads a CSV file and returns a DataFrame.
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f" Error reading '{file_path}': {e}")
        return None

def read_mapping(mapping_file):
    with open(mapping_file, "r") as f:
        data = json.load(f)
    return data.get("column_mappings", {})

