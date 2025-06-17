import pandas as pd
import json

def compare_rows_by_composite_key(source_df, dest_df, mapping_data):
    column_mappings = mapping_data["column_mappings"]
    dest_keys = ["claim_id", "patient_id", "claim_segment"]

    try:
        mapped_keys = {v: k for k, v in column_mappings.items()}
    except Exception as e:
        print("Error mapping keys:", e)
        return

    for key in dest_keys:
        if key not in dest_df.columns or mapped_keys.get(key) not in source_df.columns:
            print(f"Missing mapped key '{key}' in either dataset.")
            return

    source_df['composite_key'] = (
        source_df[mapped_keys["claim_id"]].astype(str) + "_" +
        source_df[mapped_keys["patient_id"]].astype(str) + "_" +
        source_df[mapped_keys["claim_segment"]].astype(str)
    )
    dest_df['composite_key'] = (
        dest_df["claim_id"].astype(str) + "_" +
        dest_df["patient_id"].astype(str) + "_" +
        dest_df["claim_segment"].astype(str)
    )

    source_indexed = source_df.set_index("composite_key")

    mismatches = []

    for i, dest_row in dest_df.iterrows():
        key = dest_row['composite_key']

        if key not in source_indexed.index:
            mismatches.append(f"Composite key '{key}' not found in source.")
            continue

        source_row = source_indexed.loc[key]
        if isinstance(source_row, pd.DataFrame):
            source_row = source_row.iloc[0]

        for src_col, dest_col in column_mappings.items():
            if src_col in source_row and dest_col in dest_row:
                src_val = source_row[src_col]
                dest_val = dest_row[dest_col]

                if pd.isna(src_val) and pd.isna(dest_val):
                    continue
                elif pd.isna(src_val) != pd.isna(dest_val):
                    mismatches.append(
                        f"[{key}] NULL_MISMATCH: {src_col} → {dest_col}: source='{src_val}' dest='{dest_val}'"
                    )
                else:
                    try:
                        # Compare numerically if possible
                        if float(src_val) != float(dest_val):
                            mismatches.append(
                                f"[{key}] VALUE_MISMATCH: {src_col} → {dest_col}: source='{src_val}' dest='{dest_val}'"
                            )
                    except:
                        # Fallback to string comparison if not numeric
                        if str(src_val).strip() != str(dest_val).strip():
                            mismatches.append(
                                f"[{key}] VALUE_MISMATCH: {src_col} → {dest_col}: source='{src_val}' dest='{dest_val}'"
                            )

    with open("row_mismatches.txt", "w") as f:
        for line in mismatches:
            f.write(line + "\n")

    print(f"Total mismatches: {len(mismatches)}. See 'row_mismatches.txt' for details.")

if __name__ == "__main__":
    with open("/workspaces/DataValidation/Data/src_data/insurance_mapping.json") as f:
        mapping_data = json.load(f)

    source_df = pd.read_csv("/workspaces/DataValidation/Data/src_data/insurance_claim.csv",dtype = str)
    dest_df = pd.read_csv("/workspaces/DataValidation/Data/src_data/cleaned_insurance_claim_.csv", dtype=str)

    compare_rows_by_composite_key(source_df, dest_df, mapping_data)