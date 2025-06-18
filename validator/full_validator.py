from file_read import FileReader, ColumnValidator
from basic_properties import BasicPropertiesValidator
from row_by_row_comparison import RowByRowComparator

class FullDatasetValidator:
    def __init__(self, src_path, dest_path, map_path):
        self.src_path = src_path
        self.dest_path = dest_path
        self.map_path = map_path

    def run(self):
        
        # Read files
        source_df = FileReader.read_csv(self.src_path)
        dest_df = FileReader.read_csv(self.dest_path)
        mapping = FileReader.read_json(self.map_path)
        col_mappings = mapping["column_mappings"]

        src_primary_key = "CLM_ID"
        dest_primary_key = "claim_id"

        # Run column mapping validation
        ColumnValidator.validate_column_mapping(source_df, dest_df, col_mappings)

        # Run basic dataset property validations
        validator = BasicPropertiesValidator(source_df, dest_df, col_mappings)
        validator.compare_row_count()
        validator.validate_data_types()
        validator.check_duplicate(source_df, "Source Dataset")
        validator.check_duplicate(dest_df, "Destination Dataset")
        validator.check_empty_rows(source_df, "Source Dataset")
        validator.check_empty_rows(dest_df, "Destination Dataset")

        # Drop duplicates if any duplicate exist
        source_df = source_df.drop_duplicates(subset=src_primary_key, keep='first')
        dest_df = dest_df.drop_duplicates(subset=dest_primary_key, keep='first')

        print("\nSource PK unique:", source_df[src_primary_key].is_unique)
        print("Destination PK unique:", dest_df[dest_primary_key].is_unique)

        # Row-by-row comparison check with primary key

        #dest_df.loc[0, 'claim_payment_amount'] = 999999 - sample testcase for a mismatch

        comparison = RowByRowComparator(source_df, dest_df, col_mappings, src_primary_key, dest_primary_key)
        comparison.compare()
