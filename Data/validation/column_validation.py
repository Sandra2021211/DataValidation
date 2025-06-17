import json

class ColumnValidation:
    def __init__(self, source_df, dest_df, mapping_data):
        self.source_df = source_df
        self.dest_df = dest_df
        self.mapping_data = mapping_data

    # To validate the column mappings between source and destination datasets
    def validate_column_mappings(self, source_df, destination_df, mapping_path):
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
