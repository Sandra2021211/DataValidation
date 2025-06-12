from row_count_validation import compare_row_and_column_counts
from empty_row_validation import check_empty_rows
from duplicate_validation import check_duplicates
from datatype_validation import validate_data_types
from column_validation import validate_column_mappings
from file_reader import read_mapping,read_csv
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    SOURCE = os.getenv("source_file")
    DESTINATION = os.getenv("dest_file")
    MAPPING_JSON = os.getenv("mapping_file")

    source_df = read_csv(SOURCE)
    dest_df = read_csv(DESTINATION)

# row_count_validation 
    if source_df is not None and dest_df is not None:
        compare_row_and_column_counts(source_df, dest_df)

# empty_row_validation
    check_empty_rows(source_df, "SOURCE")
    check_empty_rows(dest_df, "DESTINATION")

# duplicate_validation
    check_duplicates(source_df, "SOURCE")
    check_duplicates(dest_df, "DESTINATION")

# datatype_validation
    col_mappings = read_mapping(MAPPING_JSON)
    validate_data_types(source_df, dest_df, col_mappings)

# column_validation
    validate_column_mappings(SOURCE, DESTINATION, MAPPING_JSON)
