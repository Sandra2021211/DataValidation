import os
from dotenv import load_dotenv
#from fullValidation import FullValidator
from customValidation import CustomDatasetValidator
from without_multithread import FullValidator

def main():
    load_dotenv()

    source_path = os.getenv("source_file")  
    dest_path = os.getenv("dest_file")
    mapping_path = os.getenv("mapping_file")  

    print("\nValidation Options:")  
    print("1. Full Validation")
    print("2. Custom Validation (Choose specific checks)\n")

    choice = input("Enter your choice (1 or 2): ").strip()

    validator = FullValidator(source_path, dest_path, mapping_path)

    if choice == "1":
        validator.run_all_validations()

    elif choice == "2":
        validator = CustomDatasetValidator(
            src_path="/workspaces/DataValidation/Data/src_data/stream/src_stream.csv",
            dest_path="/workspaces/DataValidation/Data/src_data/stream/dest_stream.csv",
            map_path="/workspaces/DataValidation/Data/src_data/stream/stream_mapping.json",
            yaml_path="/workspaces/DataValidation/Data/src_data/stream/requirements.yaml"
        )
        validator.run()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()  