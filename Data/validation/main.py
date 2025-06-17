from basic_properties import BasicPropertiesValidator
from column_validation import ColumnValidation
import os
from dotenv import load_dotenv
from file_reader import read_csv, read_mapping

def main():
    load_dotenv()

    source_path = os.getenv("source_file")
    dest_path = os.getenv("dest_file")
    mapping_path = os.getenv("mapping_file")

    source_df = read_csv(source_path)
    dest_df = read_csv(dest_path)
    mapping_data = read_mapping(mapping_path)

    validator = BasicPropertiesValidator(source_df, dest_df, mapping_data)

    validator.check_empty_rows(source_df, "SOURCE")
    validator.check_empty_rows(dest_df, "DESTINATION")  

    validator.check_duplicates(source_df, "SOURCE")
    validator.check_duplicates(dest_df, "DESTINATION")  

    validator.validate_data_types(source_df, dest_df, mapping_data)

    validator.compare_row_and_column_counts(source_df, dest_df) 

    column_validator = ColumnValidation(source_df, dest_df, mapping_data)
    column_validator.validate_column_mappings(source_df, dest_df, mapping_path)


if __name__ == "__main__":
    main()

    




