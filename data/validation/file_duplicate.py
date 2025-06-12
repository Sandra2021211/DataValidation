import pandas as pd

def check_duplicates(file_path, dataset_name):
    try:
        data = pd.read_csv(file_path)
        duplicates = data[data.duplicated(keep=False)]
        
        if duplicates.empty:
            print(f"No duplicate records found in {dataset_name}.")
        else:
            print(f"Duplicate records found in {dataset_name}:")
            print(duplicates)
            print(f"Total duplicates in {dataset_name}: {len(duplicates)}")
    except Exception as e:
        print(f"Error while processing {dataset_name}: {e}")

source_file = "/workspaces/DataValidation/data/src_data/insurance_Claim_.csv" 
destination_file = "/workspaces/DataValidation/data/src_data/cleaned_insurance_claim_.csv" 

check_duplicates(source_file, "Source Dataset")
check_duplicates(destination_file, "Destination Dataset")
