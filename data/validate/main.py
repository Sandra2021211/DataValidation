# main.py

import json
from fullValidator import DataValidator
from customValidator import CustomDatasetValidator

def main():
    source_file = "/workspaces/DataValidation/data/src_data/insurance_Claim_.csv"
    destination_file = "/workspaces/DataValidation/data/src_data/cleaned_insurance_claim_.csv"
    column_mappings_path = "/workspaces/DataValidation/data/src_data/insurance_mapping.json"

    validator = DataValidator(source_file, destination_file, column_mappings_path)

    print("Choose an option:")
    print("1. Full Validator")
    print("2. Custom Validator")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        validator.compare_row_counts()
        validator.validate_data_types()
        validator.check_duplicates("Source Dataset")
        validator.check_duplicates("Destination Dataset")
        validator.identify_empty_rows("Source Dataset")
        validator.identify_empty_rows("Destination Dataset")
        validator.validate_column_mappings()
        try:
            with open(column_mappings_path) as f:
                mapping_data = json.load(f)
            validator.compare_rows()
        except Exception as e:
            print(f"Error loading mapping data: {e}")
    elif choice == "2":
        validator = CustomDatasetValidator(
            src_path="/workspaces/DataValidation/data/src_data/expanded_source.csv",
            dest_path="/workspaces/DataValidation/data/src_data/expanded_destination.csv",
            map_path="/workspaces/DataValidation/data/src_data/insurance_mapping.json",
            yaml_path="/workspaces/DataValidation/data/src_data/details.yaml"
        )
        validator.run()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
