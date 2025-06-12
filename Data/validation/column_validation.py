import json
from file_reader import read_csv 
import os
from dotenv import load_dotenv

load_dotenv()

def validate_column_mappings(source_path, destination_path, mapping_path):
    source_df = read_csv(source_path)
    destination_df = read_csv(destination_path)

    if source_df is None or destination_df is None:
        print("Error reading one or both CSV files.")
        return

    # Read JSON mapping
    try:
        with open(mapping_path) as f:
            mapping = json.load(f)
    except Exception as e:
        print(f"Error reading mapping file: {e}")
        return

    column_mappings = mapping.get("column_mappings", {})
    mapped_source_columns = set(column_mappings.keys())
    expected_destination_columns = set(column_mappings.values())

    # Get actual columns
    source_columns = set(source_df.columns)
    destination_columns = set(destination_df.columns)

    # Validate mapped columns
    valid_mapped_columns = {
        dest for src, dest in column_mappings.items() if src in source_columns
    }

    # Find unmapped destination columns
    unmapped_columns = destination_columns - valid_mapped_columns

    print("\n--- Column Mapping Validation ---")
    if unmapped_columns:
        print("Unmapped destination columns:")
        for col in unmapped_columns:
            print(f" - {col}")
    else:
        print("All destination columns are mapped from source columns.")
