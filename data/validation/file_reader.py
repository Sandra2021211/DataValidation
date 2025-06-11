import pandas as pd
import json

source_df = pd.read_csv("/workspaces/DataValidation/data/src_data/insurance_Claim_.csv")
destination_df = pd.read_csv("/workspaces/DataValidation/data/src_data/cleaned_insurance_claim_.csv")

with open("/workspaces/DataValidation/data/src_data/insurance_mapping.json") as f:
    mapping = json.load(f)

column_mappings = mapping["column_mappings"]

mapped_source_columns = set(column_mappings.keys())
expected_destination_columns = set(column_mappings.values())

source_columns = set(source_df.columns)
destination_columns = set(destination_df.columns)

valid_mapped_columns = {
    dest for src, dest in column_mappings.items() if src in source_columns
}

unmapped_columns = destination_columns - valid_mapped_columns

if unmapped_columns:
    print("Unmapped destination columns found:")
    for col in unmapped_columns:
        print(f" - {col}")
else:
    print("All destination columns are correctly mapped from source columns.")
