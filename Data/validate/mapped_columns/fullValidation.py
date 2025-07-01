import pandas as pd
import json
import itertools
import time
import numpy as np
from multiprocessing import Pool, cpu_count


def compare_row_chunk(args):
    dest_chunk, source_indexed, mapping_data = args
    mismatches = []

    for i, dest_row in dest_chunk.iterrows():
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
                    mismatches.append(
                        f"[{key}] NULL_MISMATCH: {src_col} → {dest_col}: source='{src_val}' dest='{dest_val}'"
                    )
                else:
                    try:
                        if float(src_val) != float(dest_val):
                            mismatches.append(
                                f"[{key}] VALUE_MISMATCH: {src_col} → {dest_col}: source='{src_val}' dest='{dest_val}'"
                            )
                    except:
                        if str(src_val).strip() != str(dest_val).strip():
                            mismatches.append(
                                f"[{key}] VALUE_MISMATCH: {src_col} → {dest_col}: source='{src_val}' dest='{dest_val}'"
                            )
    return mismatches


class FullValidator:
    def __init__(self, source_path, dest_path, mapping_path):
        self.source_path = source_path
        self.dest_path = dest_path
        self.mapping_path = mapping_path
        self.source_df = None
        self.dest_df = None
        self.mapping_data = {}
        self.unique_key_columns = []

        self.load_data()

    def read_csv(self, file_path):
        try:
            return pd.read_csv(file_path, dtype=str)
        except Exception as e:
            print(f"Error reading '{file_path}': {e}")
            return pd.DataFrame()

    def read_mapping(self, mapping_file):
        try:
            with open(mapping_file, "r") as f:
                data = json.load(f)
            return data.get("column_mappings", {})
        except Exception as e:
            print(f" Error reading mapping file: {e}")
            return {}

    def load_data(self):
        self.source_df = self.read_csv(self.source_path).drop_duplicates()
        self.dest_df = self.read_csv(self.dest_path)
        self.mapping_data = self.read_mapping(self.mapping_path)

    def check_empty_rows(self, df, file_name):
        empty_rows = df[df.isnull().all(axis=1)]
        count = len(empty_rows)
        print(f"\n Checking completely empty rows in {file_name} dataset:")
        print(f" Found {count} empty rows.")
        return count

    def check_duplicates(self, df, file_name):
        duplicates = df[df.duplicated()]
        count = len(duplicates)
        print(f"\n Checking duplicate rows in {file_name} dataset:")
        print(f" Found {count} duplicate records.")
        return count

    def validate_data_types(self):
        mismatch = []
        for src, dest in self.mapping_data.items():
            if src in self.source_df.columns and dest in self.dest_df.columns:
                src_dtype = str(self.source_df[src].dtype)
                dest_dtype = str(self.dest_df[dest].dtype)
                if src_dtype != dest_dtype:
                    mismatch.append((src, dest, src_dtype, dest_dtype))

        print("\n Data Type Validation:")
        if mismatch:
            for src_col, dest_col, src_type, dest_type in mismatch:
                print(f" {src_col} ({src_type}) ≠ {dest_col} ({dest_type})")
        else:
            print(" All column data types match.")

    def compare_row_and_column_counts(self):
        source_rows, source_cols = self.source_df.shape
        dest_rows, dest_cols = self.dest_df.shape

        print("\nRow and Column Count Comparison:")
        print(f"Source:      {source_rows} rows × {source_cols} columns")
        print(f"Destination: {dest_rows} rows × {dest_cols} columns")
        print(f" Row count {'matches' if source_rows == dest_rows else 'does not match'}")
        print(f" Column count {'matches' if source_cols == dest_cols else 'does not match'}")

    def validate_column_mappings(self):
        column_mappings = self.mapping_data
        source_columns = set(self.source_df.columns)
        dest_columns = set(self.dest_df.columns)

        mapped_source_columns = set(column_mappings.keys())
        expected_dest_columns = set(column_mappings.values())
        valid_mapped_dest = {
            dest for src, dest in column_mappings.items() if src in source_columns
        }

        unmapped_dest_columns = dest_columns - valid_mapped_dest

        print("\n Column Mapping Validation:")
        if unmapped_dest_columns:
            print(" Unmapped destination columns:")
            for col in unmapped_dest_columns:
                print(f" - {col}")
        else:
            print(" All destination columns are mapped.")

    def find_min_unique_key(self):
        cols = self.dest_df.columns.tolist()
        for r in range(1, len(cols) + 1):
            for combo in itertools.combinations(cols, r):
                if self.dest_df.duplicated(subset=combo).sum() == 0:
                    self.unique_key_columns = list(combo)
                    return
        self.unique_key_columns = []

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

        # Split dest_df into chunks for multiprocessing
        num_processes = min(cpu_count(), 4)  # Limit to 4 or available cores
        chunks = np.array_split(self.dest_df, num_processes)

        # Prepare arguments
        args = [(chunk, source_indexed, self.mapping_data) for chunk in chunks]

        with Pool(processes=num_processes) as pool:
            results = pool.map(compare_row_chunk, args)

        # Flatten results
        mismatches = [line for sublist in results for line in sublist]

        with open("row_mismatches.txt", "w") as f:
            for line in mismatches:
                f.write(line + "\n")

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"\n Row comparison complete. Mismatches found: {len(mismatches)}")
        print(" See 'row_mismatches.txt' for details.")
        print(f" Time taken: {elapsed_time:.2f} seconds")

    def run_all_validations(self):
        self.check_empty_rows(self.source_df, "SOURCE")
        self.check_empty_rows(self.dest_df, "DESTINATION")
        self.check_duplicates(self.source_df, "SOURCE")
        self.check_duplicates(self.dest_df, "DESTINATION")
        self.validate_data_types()
        self.compare_row_and_column_counts()
        self.validate_column_mappings()
        self.compare_rows()