from full_validator import FullDatasetValidator
from custom_validator import CustomDatasetValidator

def main():
    print("\nChoose Validation Mode:")
    print("1. Full Dataset Validation")
    print("2. Custom Dataset Window (Corrupted Range) Validation")

    choice = input("Enter 1 or 2: ").strip()

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

if __name__ == "__main__":
    main()
