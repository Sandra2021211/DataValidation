import pandas as pd

def identify_empty_rows(file_path, dataset_name):
   
    try:
        data = pd.read_csv(file_path)
        
        empty_rows = data[data.isnull().all(axis=1)]

        if empty_rows.empty:
            print(f"No completely empty rows found in {dataset_name}.")
        else:
            print(f"Completely empty rows found in {dataset_name}:")
            print(empty_rows)
            print(f"Total completely empty rows in {dataset_name}: {len(empty_rows)}")
    except Exception as e:
        print(f"Error while processing {dataset_name}: {e}")

source_file = "/workspaces/DataValidation/data/src_data/insurance_Claim_.csv"  
destination_file = "/workspaces/DataValidation/data/src_data/cleaned_insurance_claim_.csv"

identify_empty_rows(source_file, "Source Dataset")
identify_empty_rows(destination_file, "Destination Dataset")
