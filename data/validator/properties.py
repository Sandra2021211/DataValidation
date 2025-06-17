import pandas as pd
import json

class DataValidator:
    def __init__(self, source_file, destination_file, column_mappings_path=None):
        self.source_file = source_file
        self.destination_file = destination_file
        self.column_mappings = None
        
        if column_mappings_path:
            self.column_mappings = self._read_json(column_mappings_path).get('column_mappings', {})
    
    @staticmethod
    def _read_json(file_path):
        try:
            with open(file_path) as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return {}
    
    def compare_row_counts(self):
        try:
            source_data = pd.read_csv(self.source_file)
            destination_data = pd.read_csv(self.destination_file)
            
            source_count = len(source_data)
            destination_count = len(destination_data)
            
            if source_count == destination_count:
                print(f"Row count matches: {source_count} rows in both files.")
            else:
                print(f"Row count mismatch: Source has {source_count} rows, Destination has {destination_count} rows.")
        except Exception as e:
            print(f"Error comparing row counts: {e}")
    
    def validate_data_types(self):
        if not self.column_mappings:
            print("Column mappings are not provided. Skipping data type validation.")
            return
        
        try:
            source_data = pd.read_csv(self.source_file)
            destination_data = pd.read_csv(self.destination_file)
            
            mismatched_types = []
            for source_col, dest_col in self.column_mappings.items():
                if source_col not in source_data.columns:
                    print(f"Source column '{source_col}' not found in source file.")
                    return
                if dest_col not in destination_data.columns:
                    print(f"Destination column '{dest_col}' not found in destination file.")
                    return
                
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
            print(f"Error validating data types: {e}")
    
    def check_duplicates(self, dataset_name="Source Dataset"):
        file_path = self.source_file if dataset_name == "Source Dataset" else self.destination_file
        try:
            data = pd.read_csv(file_path)
            duplicates = data[data.duplicated(keep=False)]
            
            if duplicates.empty:
                print(f"No duplicate records found in {dataset_name}.")
            else:
                print(f"Duplicate records found in {dataset_name}:")
                print(duplicates)
                print(f"Total duplicates in {dataset_name}: {len(duplicates)}")
        except Exception as e:
            print(f"Error checking duplicates in {dataset_name}: {e}")
    
    def identify_empty_rows(self, dataset_name="Source Dataset"):
        file_path = self.source_file if dataset_name == "Source Dataset" else self.destination_file
        try:
            data = pd.read_csv(file_path)
            empty_rows = data[data.isnull().all(axis=1)]
            
            if empty_rows.empty:
                print(f"No completely empty rows found in {dataset_name}.")
            else:
                print(f"Completely empty rows found in {dataset_name}:")
                print(empty_rows)
                print(f"Total completely empty rows in {dataset_name}: {len(empty_rows)}")
        except Exception as e:
            print(f"Error identifying empty rows in {dataset_name}: {e}")

source_file = "/workspaces/DataValidation/data/src_data/insurance_Claim_.csv"
destination_file = "/workspaces/DataValidation/data/src_data/cleaned_insurance_claim_.csv"
column_mappings_path = "/workspaces/DataValidation/data/src_data/insurance_mapping.json"

validator = DataValidator(source_file, destination_file, column_mappings_path)

validator.compare_row_counts()
validator.validate_data_types()
validator.check_duplicates("Source Dataset")
validator.check_duplicates("Destination Dataset")
validator.identify_empty_rows("Source Dataset")
validator.identify_empty_rows("Destination Dataset")
