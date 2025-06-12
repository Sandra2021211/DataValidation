import pandas as pd
import json

def read_json(column_mappings_path):
    with open(column_mappings_path) as f:
        return json.load(f)

def validate_data_types(source_file, destination_file, column_mappings):
    try:
        source_data = pd.read_csv(source_file)
        destination_data = pd.read_csv(destination_file)
        
        for source_col, dest_col in column_mappings.items():
            if source_col not in source_data.columns:
                print(f"Source column '{source_col}' not found in source file.")
                return
            if dest_col not in destination_data.columns:
                print(f"Destination column '{dest_col}' not found in destination file.")
                return
                     
        mismatched_types = []
        for source_col, dest_col in column_mappings.items():
            source_dtype = str(source_data[source_col].dtype)
            destination_dtype = str(destination_data[dest_col].dtype)

            if source_dtype != destination_dtype:
                mismatched_types.append((source_col, dest_col, source_dtype, destination_dtype))
        
        if not mismatched_types:
            print("All mapped columns have consistent data types.")
        else:
            print("Data type mismatches found:")
            for source_col, dest_col, source_dtype, destination_dtype in mismatched_types:
                print(f"  Source column '{source_col}' (type: {source_dtype}) "
                      f"does not match Destination column '{dest_col}' (type: {destination_dtype}).")
    except Exception as e:
        print(f"Error: {e}")

source_file = "/workspaces/DataValidation/data/src_data/insurance_Claim_.csv"
destination_file = "/workspaces/DataValidation/data/src_data/cleaned_insurance_claim_.csv"
column_mappings_path = "/workspaces/DataValidation/data/src_data/insurance_mapping.json"

mapping = read_json(column_mappings_path)
maps = mapping['column_mappings']

validate_data_types(source_file, destination_file, maps)
