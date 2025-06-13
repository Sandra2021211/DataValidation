from file_read import FileReader, ColumnValidator
from basic_properties import BasicPropertiesValidator

def main():
    # Define paths
    src_path = "src_data/insurance_claims.csv"
    dest_path = "src_data/cleaned_insurance_claims.csv"
    map_path = "src_data/mapping.json"

    # Read files
    source_df = FileReader.read_csv(src_path)
    dest_df = FileReader.read_csv(dest_path)
    mapping = FileReader.read_json(map_path)
    col_mappings = mapping["column_mappings"]

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

if __name__ == "__main__":
    main()

