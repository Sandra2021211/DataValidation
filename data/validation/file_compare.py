import pandas as pd

def compare_row_counts(source_file, destination_file):
    try:
        source_data = pd.read_csv(source_file)
        destination_data = pd.read_csv(destination_file)
        
        source_count = len(source_data)
        destination_count = len(destination_data)
        
        if source_count == destination_count:
            print(f"Row count matches: {source_count} rows in both files.")
        else:
            print(f"Row count mismatch: Source has {source_count} rows, Destination has {destination_count} rows.")
    
    except Exception as e:
        print(f"Error: {e}")

source_file = "/workspaces/DataValidation/data/src_data/insurance_Claim_.csv"  
destination_file = "/workspaces/DataValidation/data/src_data/cleaned_insurance_claim_.csv" 

compare_row_counts(source_file, destination_file)
