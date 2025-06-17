from properties import DataValidator
from column_mappings import ColumnMappingValidator

source_file = "/workspaces/DataValidation/data/src_data/insurance_Claim_.csv"
destination_file = "/workspaces/DataValidation/data/src_data/cleaned_insurance_claim_.csv"
column_mappings_path = "/workspaces/DataValidation/data/src_data/insurance_mapping.json"

validator = DataValidator(source_file, destination_file, column_mappings_path)

print("Comparing row counts...")
validator.compare_row_counts()

print("\nValidating data types...")
validator.validate_data_types()

print("\nChecking duplicates in Source Dataset...")
validator.check_duplicates("Source Dataset")

print("\nChecking duplicates in Destination Dataset...")
validator.check_duplicates("Destination Dataset")

print("\nIdentifying empty rows in Source Dataset...")
validator.identify_empty_rows("Source Dataset")

print("\nIdentifying empty rows in Destination Dataset...")
validator.identify_empty_rows("Destination Dataset")

column_validator = ColumnMappingValidator(source_file, destination_file, column_mappings_path)

print("\nValidating column mappings...")
column_validator.load_data()
column_validator.validate_mappings()