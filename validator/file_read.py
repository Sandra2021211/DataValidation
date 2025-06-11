import pandas as pd
import json

def read_csv(path):
    """Reads a CSV file and returns a DataFrame."""
    return pd.read_csv(path)

def read_json(path):
    """Reads a JSON file and returns a dictionary."""
    with open(path, 'r') as f:
        return json.load(f)

def column_validator(source_df, destination_df, column_mappings):
    """Validates that all destination columns have corresponding mapped source columns."""

    source_columns = set(source_df.columns)
    destination_columns = set(destination_df.columns)

    valid_mapped_columns = {
        dest for src, dest in column_mappings.items() if src in source_columns
    }

    unmapped_columns = destination_columns - valid_mapped_columns

    if unmapped_columns:
        print("Unmapped destination columns found:")
        for col in unmapped_columns:
            print(f" - {col}")
    else:
        print("All destination columns are correctly mapped from source columns.")

if __name__ == "__main__":
    source_csv = "src_data/insurance_claims.csv"
    destination_csv = "src_data/cleaned_insurance_claims.csv"
    mapping_file = "src_data/mapping.json"

    source_df = read_csv(source_csv)
    destination_df = read_csv(destination_csv)
    mapping = read_json(mapping_file)

    column_mappings = mapping["column_mappings"]

    column_validator(source_df, destination_df, column_mappings)
