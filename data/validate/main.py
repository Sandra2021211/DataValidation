import json
from fullValidator import DataValidator
from customValidator import CustomDatasetValidator
from column_matcher import ColumnMatcher 

def main():
    print("Choose an option:")
    print("1. Full Validator")
    print("2. Custom Validator")
    print("3. Column Matcher Without Predefined Mapping") 

    choice = input("Enter your choice (1, 2, or 3): ")

    try:
        if choice == "1":
            # Full Validator
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
            validator.validate_column_mappings()
            try:
                with open(column_mappings_path) as f:
                    mapping_data = json.load(f)
                validator.compare_rows()
            except Exception as e:
                print(f"Error loading mapping data: {e}")

        elif choice == "2":
            # Custom Validator
            validator = CustomDatasetValidator(
                src_path="/workspaces/DataValidation/data/src_data/expanded_source.csv",
                dest_path="/workspaces/DataValidation/data/src_data/expanded_destination.csv",
                map_path="/workspaces/DataValidation/data/src_data/insurance_mapping.json",
                yaml_path="/workspaces/DataValidation/data/src_data/details.yaml"
            )
            validator.run()

        elif choice == "3":
            # Column Matcher Without Predefined Mapping
            matcher = ColumnMatcher(
                source_path="/workspaces/DataValidation/data/src_data/SRC.csv",
                destination_path="/workspaces/DataValidation/data/src_data/DST.csv",
                source_key="Salary", 
                destination_key="Annual_Salary"  
            )
            matcher.execute()

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format in file: {e}")
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    main()
