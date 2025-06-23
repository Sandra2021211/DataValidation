import pandas as pd
import numpy as np
import json
import time
from multiprocessing import Pool, cpu_count

# Worker function for row-level comparison (used in each process)
def compare_row_chunk(args):
    chunk_df, source_indexed, mapping_data = args
    mismatches = []

    for _, dest_row in chunk_df.iterrows():
        key = dest_row["composite_key"]
        if key not in source_indexed.index:
            mismatches.append(f" Composite key '{key}' not found in source.")
            continue

        source_row = source_indexed.loc[key]
        if isinstance(source_row, pd.DataFrame):
            source_row = source_row.iloc[0]

        for src_col, dest_col in mapping_data.items():
            if src_col in source_row and dest_col in dest_row:
                src_val = source_row[src_col]
                dest_val = dest_row[dest_col]

                if pd.isna(src_val) and pd.isna(dest_val):
                    continue
                elif pd.isna(src_val) != pd.isna(dest_val):
                    mismatches.append(f"[{key}] NULL_MISMATCH: {src_col} → {dest_col}: source='{src_val}' dest='{dest_val}'")
                else:
                    try:
                        if float(src_val) != float(dest_val):
                            mismatches.append(f"[{key}] VALUE_MISMATCH: {src_col} → {dest_col}: source='{src_val}' dest='{dest_val}'")
                    except:
                        if str(src_val).strip() != str(dest_val).strip():
                            mismatches.append(f"[{key}] VALUE_MISMATCH: {src_col} → {dest_col}: source='{src_val}' dest='{dest_val}'")
    return mismatches


class FullValidator:
    def __init__(self, source_path, dest_path, mapping_path):
        self.source_path = source_path
        self.dest_path = dest_path
        self.mapping_path = mapping_path
        self.mapping_data = {}
        self.source_df = None
        self.dest_df = None
        self.unique_key_columns = []
        self.load_data()

    def load_data(self):
        self.source_df = pd.read_csv(self.source_path)
        self.dest_df = pd.read_csv(self.dest_path)
        with open(self.mapping_path) as f:
            full_config = json.load(f)
            self.mapping_data = full_config.get("column_mappings", {})
            self.primary_key = full_config.get("validation_rules", {}).get("primary_key")

    def find_min_unique_key(self):
        # Hardcoded composite key: claim_id + claim_segment
        self.unique_key_columns = ["claim_id", "claim_segment"]

    def compare_rows(self):
        self.find_min_unique_key()
        start_time = time.time()

        if not self.unique_key_columns:
            print("\n No unique key combination found.")
            return

        print("\n Unique key combination for row-level comparison:")
        print(f" Columns: {self.unique_key_columns}")

        mapped_keys = {v: k for k, v in self.mapping_data.items()}

        for key in self.unique_key_columns:
            if key not in self.dest_df.columns or mapped_keys.get(key) not in self.source_df.columns:
                print(f" Mapped key '{key}' missing in one of the datasets.")
                return

        self.source_df["composite_key"] = self.source_df[
            [mapped_keys[k] for k in self.unique_key_columns]
        ].astype(str).agg("_".join, axis=1)

        self.dest_df["composite_key"] = self.dest_df[
            self.unique_key_columns
        ].astype(str).agg("_".join, axis=1)

        source_indexed = self.source_df.set_index("composite_key")

        # Prepare chunks and arguments
        num_processes = min(cpu_count(), 4)
        chunks = np.array_split(self.dest_df, num_processes)
        args = [(chunk, source_indexed, self.mapping_data) for chunk in chunks]

        # Multiprocessing pool
        with Pool(processes=num_processes) as pool:
            results = pool.map(compare_row_chunk, args)

        # Combine mismatches from all processes
        mismatches = [m for result in results for m in result]

        with open("row_mismatches.txt", "w") as f:
            for line in mismatches:
                f.write(line + "\n")

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"\n Row comparison complete. Mismatches found: {len(mismatches)}")
        print(" See 'row_mismatches.txt' for details.")
        print(f" Time taken: {elapsed_time:.2f} seconds")


# Run script
if __name__ == "__main__":
    validator = FullValidator(
        "/workspaces/DataValidation/Data/src_data/insurance_claim.csv",
        "/workspaces/DataValidation/Data/src_data/cleaned_insurance_claim_.csv",
        "/workspaces/DataValidation/Data/src_data/insurance_mapping.json"
    )
    validator.compare_rows()