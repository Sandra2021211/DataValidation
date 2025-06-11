import pandas as pd
import json

#function to read_csv files
source_df = pd.read_csv("/workspaces/DataValidation/Data/src_data/insurance_claim.csv")
destination_df = pd.read_csv("/workspaces/DataValidation/Data/src_data/cleaned_insurance_claim_.csv")
 
#function to open and read_json  
with open("/workspaces/DataValidation/Data/src_data/insurance_mapping.json") as f:
    mapping = json.load(f)
 
#Extraction from json
column_mappings = mapping["column_mappings"]
mapped_source_columns = set(column_mappings.keys())

#print(mapped_source_columns)
expected_destination_columns = set(column_mappings.values())

#Create sets of the source column and the expected destination column
source_columns = set(source_df.columns)
destination_columns = set(destination_df.columns)
 
valid_mapped_columns = {
    dest for src, dest in column_mappings.items() if src in source_columns
}

#perform set difference to find umapped col
unmapped_columns = destination_columns - valid_mapped_columns
 
if unmapped_columns:
    print("Unmapped destination columns :")
    for col in unmapped_columns:
        print(f" - {col}")
else:
    print("All destination columns are mapped from source columns.")
 