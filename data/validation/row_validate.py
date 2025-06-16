import pandas as pd
import json
 
def compare_rows_by_claim_id(src_df, dst_df, mapping_data):
    column_mappings = mapping_data["column_mappings"]
    primary_key = mapping_data["validation_rules"]["primary_key"]
 
    for src_col, dest_col in column_mappings.items():
        if dest_col == primary_key:
            source_key = src_col
            break
 
    if source_key is None:
        print("Could not find source primary key for the destination primary key.")
        return
    if primary_key not in dst_df.columns or source_key not in src_df.columns:
        print("Primary key column is missing in one of the datasets.")
        return
 
    mismatches = []
 
    for i, dest_row in dst_df.iterrows():
        claim_id = dest_row[primary_key]
 
        source_row = src_df[src_df[source_key] == claim_id]
 
        if source_row.empty:
            mismatches.append(f"Destination claim_id '{claim_id}' not found in source.\n")
            continue
 
        source_row = source_row.iloc[0]
 
        for src_col, dest_col in column_mappings.items():
            if src_col in source_row and dest_col in dest_row:
                src_val = source_row[src_col]
                dest_val = dest_row[dest_col]
 
                if pd.isna(src_val) and pd.isna(dest_val):
                    continue  # both are NaN → OK
                elif pd.isna(src_val) != pd.isna(dest_val) or str(src_val) != str(dest_val):
                    mismatches.append(
                        f"ID {claim_id}: {src_col} -> {dest_col} mismatch: source='{src_val}' destination='{dest_val}'"
                    )
 
    with open("mismatches.txt", "w") as f:
        for line in mismatches:
            f.write(line + "\n")
 
    print(f"Total mismatches found: {len(mismatches)}")
 
if __name__ == "__main__":

    with open("/workspaces/DataValidation/data/src_data/insurance_mapping.json") as f:
        mapping_data = json.load(f)
 
    src_df = pd.read_csv("/workspaces/DataValidation/data/src_data/insurance_Claim_.csv")
    dst_df = pd.read_csv("/workspaces/DataValidation/data/src_data/cleaned_insurance_claim_.csv")
    compare_rows_by_claim_id(src_df, dst_df, mapping_data)