from full_validator import FullDatasetValidator
from custom_validator import CustomDatasetValidator
import json 
import yaml
import sys
import pandas as pd 

def main():
    print("\nChoose Validation Mode:")
    print("1. Full Dataset Validation")
    print("2. Custom Dataset Validation")

    choice = input("Enter 1 or 2: ").strip()

    try:
        if choice == "1":
            validator = FullDatasetValidator(
                src_path="src_data/insurance_claims.csv",
                dest_path="src_data/cleaned_insurance_claims.csv",
                map_path="src_data/mapping.json"
            )
            validator.run()

        elif choice == "2":
            validator = CustomDatasetValidator(
                src_path="src_data/src_with_stream_time.csv",
                dest_path="src_data/destination_with_stream_time.csv",
                map_path="src_data/mapping.json",
                yaml_path="src_data/requirements.yaml"
            )
            validator.run()

        else:
            print("Invalid input. Please enter 1 or 2.")

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format in file: {e}")
    except yaml.YAMLError as e:
        print(f"Invalid YAML format in file: {e}")
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
        sys.exit(1)
    

if __name__ == "__main__":
    main()
