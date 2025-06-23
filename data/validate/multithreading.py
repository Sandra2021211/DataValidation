import json
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


class RowByRowComparator:
    def __init__(self, source_df, dest_df, col_mappings, src_primary_key, dest_primary_key):
        self.source_df = source_df.copy()
        self.dest_df = dest_df.copy()
        self.col_mappings = col_mappings
        self.src_primary_key = src_primary_key
        self.dest_primary_key = dest_primary_key

        # Set index for fast row access using primary key
        self.source_df.set_index(src_primary_key, inplace=True)
        self.dest_df.set_index(dest_primary_key, inplace=True)

    def compare_row(self, k):
        mismatch = []

        if k not in self.dest_df.index:
            mismatch.append((k, "row", "missing in destination"))
            return mismatch

        # Convert rows to dictionaries for scalar access
        src_row = self.source_df.loc[k].to_dict()
        dest_row = self.dest_df.loc[k].to_dict()

        for src_col, dest_col in self.col_mappings.items():
            if src_col in src_row and dest_col in dest_row:
                src_val = src_row[src_col]
                dest_val = dest_row[dest_col]

                # Ensure values are scalars and check for nulls
                if pd.isnull(src_val) and pd.isnull(dest_val):
                    continue

                # Compare scalar values
                if src_val != dest_val:
                    mismatch.append((k, src_col, dest_col, src_val, dest_val))
        return mismatch

    def compare(self):
        print("\nRow by Row comparison:")
        start_time = time.time()
        all_mismatch = []

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(self.compare_row, k) for k in self.source_df.index]

            for future in as_completed(futures):
                mismatch = future.result()
                if mismatch:
                    all_mismatch.extend(mismatch)

        if all_mismatch:
            print("Mismatches found:")
            for mis in all_mismatch:
                if len(mis) == 3:
                    print(f"Row {mis[0]}: {mis[2]}")
                else:
                    print(f"Row {mis[0]} | Source: {mis[1]}-{mis[3]} , Destination: {mis[2]}-{mis[4]}")
        else:
            print("All rows match!!!")

        end_time = time.time()
        print(f"Time taken for row-by-row comparison: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    source_file_path = "/workspaces/DataValidation/data/src_data/insurance_Claim_.csv"
    destination_file_path = "/workspaces/DataValidation/data/src_data/cleaned_insurance_claim_.csv"
    mapping_file_path = "/workspaces/DataValidation/data/src_data/insurance_mapping.json"

    try:
        # Load mapping JSON
        with open(mapping_file_path, 'r') as f:
            mapping = json.load(f)

        # Extract column mappings and primary keys
        column_mappings = mapping.get("column_mappings", {})
        primary_key = mapping["validation_rules"]["primary_key"]

        # Load datasets with normalized column names
        source_df = pd.read_csv(source_file_path)
        destination_df = pd.read_csv(destination_file_path)

        # Rename columns according to mapping
        source_df.rename(columns={k: v for k, v in column_mappings.items()}, inplace=True)

        # Ensure primary key exists in both datasets
        if primary_key not in source_df.columns:
            raise KeyError(f"Primary key '{primary_key}' not found in source file columns")
        if primary_key not in destination_df.columns:
            raise KeyError(f"Primary key '{primary_key}' not found in destination file columns")

        # Instantiate the comparator
        comparator = RowByRowComparator(
            source_df=source_df,
            dest_df=destination_df,
            col_mappings=column_mappings,
            src_primary_key=primary_key,
            dest_primary_key=primary_key
        )

        # Perform comparison
        comparator.compare()

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except KeyError as e:
        print(f"Key error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
