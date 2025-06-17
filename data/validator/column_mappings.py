import pandas as pd
import json

class ColumnMappingValidator:
    def __init__(self, source_file, destination_file, mapping_file):
        self.source_file = source_file
        self.destination_file = destination_file
        self.mapping_file = mapping_file
        self.source_df = None
        self.destination_df = None
        self.column_mappings = None

    def load_data(self):
        try:
            self.source_df = pd.read_csv(self.source_file)
            self.destination_df = pd.read_csv(self.destination_file)
            with open(self.mapping_file) as f:
                self.column_mappings = json.load(f).get("column_mappings", {})
        except Exception as e:
            print(f"Error loading data or mappings: {e}")

    def validate_mappings(self):
        if self.source_df is None or self.destination_df is None or self.column_mappings is None:
            print("Data or mappings are not loaded. Run load_data() first.")
            return

        mapped_source_columns = set(self.column_mappings.keys())
        expected_destination_columns = set(self.column_mappings.values())

        source_columns = set(self.source_df.columns)
        destination_columns = set(self.destination_df.columns)

        valid_mapped_columns = {
            dest for src, dest in self.column_mappings.items() if src in source_columns
        }

        unmapped_columns = destination_columns - valid_mapped_columns

        if unmapped_columns:
            print("Unmapped destination columns found:")
            for col in unmapped_columns:
                print(f" - {col}")
        else:
            print("All destination columns are correctly mapped from source columns.")

if __name__ == "__main__":
    source_file = "/workspaces/DataValidation/data/src_data/insurance_Claim_.csv"
    destination_file = "/workspaces/DataValidation/data/src_data/cleaned_insurance_claim_.csv"
    mapping_file = "/workspaces/DataValidation/data/src_data/insurance_mapping.json"

    validator = ColumnMappingValidator(source_file, destination_file, mapping_file)
    validator.load_data()
    validator.validate_mappings()
