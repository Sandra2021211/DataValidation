import pandas as pd
import json
import yaml

class FileReader:
    @staticmethod
    def read_csv(path, **kwargs):
        #Reads a CSV file and returns a DataFrame.
        try:
            return pd.read_csv(path, **kwargs)
        except FileNotFoundError:
            print(f"CSV file not found: {path}") 

    @staticmethod
    def read_json(path):
        #Reads a JSON file and returns a dictionary.
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"JSON file not found: {path}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {path}: {e}")

    @staticmethod
    def read_yaml(path):
        try:
            with open(path,'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"YAML file not found: {path}")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML in {path}: {e}")

class ColumnValidator:
    @staticmethod
    def validate_column_mapping(source_df, destination_df, column_mappings):
        #Validates that all destination columns have corresponding mapped source columns.
        try:
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
        except KeyError as e:
            print(f"Missing key in column mapping: {e}")
        except Exception as e:
            print(f"Unexpected error during column validation: {type(e).__name__}: {e}")
