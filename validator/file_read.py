import pandas as pd
import json

class FileReader:
    @staticmethod
    def read_csv(path):
        #Reads a CSV file and returns a DataFrame.
        return pd.read_csv(path)

    @staticmethod
    def read_json(path):
        #Reads a JSON file and returns a dictionary.
        with open(path, 'r') as f:
            return json.load(f)

class ColumnValidator:
    @staticmethod
    def validate_column_mapping(source_df, destination_df, column_mappings):
        """Validates that all destination columns have corresponding mapped source columns."""
        source_columns = set(source_df.columns)
        destination_columns = set(destination_df.columns)

        valid_mapped_columns = {
            dest for src, dest in column_mappings.items() if src in source_columns
        }

        unmapped_columns = destination_columns - valid_mapped_columns

        print("\nColumn Mapping Validation:")
        if unmapped_columns:
            print("Unmapped destination columns found:")
            for col in unmapped_columns:
                print(f" - {col}")
        else:
            print("All destination columns are correctly mapped.")
