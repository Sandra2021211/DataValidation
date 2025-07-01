import os
from dotenv import load_dotenv
from mapped_columns.customValidation import CustomDatasetValidator
from mapped_columns.without_multithread import FullValidator
from unmapped_columns.UnmappedColumnValidator import UnmappedColumnValidator

def main():
    load_dotenv()

    source_path = os.getenv("source_file")  
    dest_path = os.getenv("dest_file")
    mapping_path = os.getenv("mapping_file")  

    print("\nValidation Options:")
    print("1. Full Validation")
    print("2. Custom Validation")
    print("3. Unmapped Column Validation\n")  

    choice = input("Enter your choice (1, 2 or 3): ").strip()

    if choice == "1":
        validator = FullValidator(source_path, dest_path, mapping_path)
        validator.run_all_validations()

    elif choice == "2":
        validator = CustomDatasetValidator(
            src_path="/workspaces/DataValidation/Data/src_data/stream/src_stream.csv",
            dest_path="/workspaces/DataValidation/Data/src_data/stream/dest_stream.csv",
            map_path="/workspaces/DataValidation/Data/src_data/stream/stream_mapping.json",
            yaml_path="/workspaces/DataValidation/Data/src_data/stream/requirements.yaml"
        )
        validator.run()

    elif choice == "3":
        validator = UnmappedColumnValidator(
            src_path="/workspaces/DataValidation/Data/src_data/insurance_claim.csv",
            dest_path="/workspaces/DataValidation/Data/src_data/cleaned_insurance_claim_.csv"
        )
        validator.run_validation()

    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()