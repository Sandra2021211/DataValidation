import pandas as pd
import json
import time
import itertools

class DataValidator:
    def __init__(self, source_file, destination_file, column_mappings_path=None):
        self.source_file = source_file
        self.destination_file = destination_file
        self.column_mappings = None

        if column_mappings_path:
            self.column_mappings = self._read_json(column_mappings_path).get('column_mappings', {})

    @staticmethod
    def _read_json(file_path):
        try:
            with open(file_path) as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return {}

    def compare_row_counts(self):
        try:
            source_data = pd.read_csv(self.source_file)
            destination_data = pd.read_csv(self.destination_file)

            source_count = len(source_data)
            destination_count = len(destination_data)

            if source_count == destination_count:
                print(f"Row count matches: {source_count} rows in both files.")
            else:
                print(f"Row count mismatch: Source has {source_count} rows, Destination has {destination_count} rows.")
        except Exception as e:
            print(f"Error comparing row counts: {e}")

    def validate_data_types(self):
        if not self.column_mappings:
            print("Column mappings are not provided. Skipping data type validation.")
            return

        try:
            source_data = pd.read_csv(self.source_file)
            destination_data = pd.read_csv(self.destination_file)

            mismatched_types = []
            for source_col, dest_col in self.column_mappings.items():
                if source_col not in source_data.columns:
                    print(f"Source column '{source_col}' not found in source file.")
                    return
                if dest_col not in destination_data.columns:
                    print(f"Destination column '{dest_col}' not found in destination file.")
                    return

                source_dtype = str(source_data[source_col].dtype)
                destination_dtype = str(destination_data[dest_col].dtype)

                if source_dtype != destination_dtype:
                    mismatched_types.append((source_col, dest_col, source_dtype, destination_dtype))

            if not mismatched_types:
                print("All mapped columns have consistent data types.")
            else:
                print("Data type mismatches found:")
                for source_col, dest_col, source_dtype, destination_dtype in mismatched_types:
                    print(f"  Source column '{source_col}' (type: {source_dtype}) "
                          f"does not match Destination column '{dest_col}' (type: {destination_dtype}).")
        except Exception as e:
            print(f"Error validating data types: {e}")

    def check_duplicates(self, dataset_name="Source Dataset"):
        file_path = self.source_file if dataset_name == "Source Dataset" else self.destination_file
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
            print(f"Error checking duplicates in {dataset_name}: {e}")

    def identify_empty_rows(self, dataset_name="Source Dataset"):
        file_path = self.source_file if dataset_name == "Source Dataset" else self.destination_file
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
            print(f"Error identifying empty rows in {dataset_name}: {e}")

    def validate_column_mappings(self):
        try:
            source_data = pd.read_csv(self.source_file)
            destination_data = pd.read_csv(self.destination_file)

            mapped_source_columns = set(self.column_mappings.keys())
            expected_destination_columns = set(self.column_mappings.values())

            source_columns = set(source_data.columns)
            destination_columns = set(destination_data.columns)

            valid_mapped_columns = {
                dest for src, dest in self.column_mappings.items() if src in source_columns
            }

            unmapped_columns = destination_columns - valid_mapped_columns

            if unmapped_columns:
                print("Unmapped destination columns found:")
                for col in unmapped_columns:
                    print(f" - {col}")
            else:
                print("All destination columns are correctly mapped from source columns.")
        except Exception as e:
            print(f"Error validating column mappings: {e}")

    def find_min_unique_key(self, data):
        cols = data.columns.tolist()
        for r in range(1, len(cols) + 1):
            for combo in itertools.combinations(cols, r):
                if data.duplicated(subset=combo).sum() == 0:
                    return list(combo)
        return []

    def compare_rows(self):
        try:
            # Load datasets
            source_data = pd.read_csv(self.source_file)
            destination_data = pd.read_csv(self.destination_file)

            # Identify the unique key combination for the destination dataset
            unique_key_columns = self.find_min_unique_key(destination_data)
            start_time = time.time()

            if not unique_key_columns:
                print("\nNo unique key combination found in the destination dataset.")
                return

            print("\nUnique key combination for row-level comparison:")
            print(f"Columns: {unique_key_columns}")

            # Map destination keys to source keys
            mapped_keys = {v: k for k, v in self.column_mappings.items()}

            # Ensure mapped keys exist in both datasets
            for key in unique_key_columns:
                if key not in destination_data.columns or mapped_keys.get(key) not in source_data.columns:
                    print(f"Mapped key '{key}' missing in one of the datasets.")
                    return

            # Create composite keys
            source_data["composite_key"] = source_data[
                [mapped_keys[k] for k in unique_key_columns]
            ].astype(str).agg("_".join, axis=1)

            destination_data["composite_key"] = destination_data[
                unique_key_columns
            ].astype(str).agg("_".join, axis=1)

            # Compare rows using composite keys
            source_indexed = source_data.set_index("composite_key")
            mismatches = []

            for i, dest_row in destination_data.iterrows():
                key = dest_row["composite_key"]
                if key not in source_indexed.index:
                    mismatches.append(f"Composite key '{key}' not found in source.")
                    continue

                source_row = source_indexed.loc[key]
                if isinstance(source_row, pd.DataFrame):
                    source_row = source_row.iloc[0]

                for src_col, dest_col in self.column_mappings.items():
                    if src_col in source_row and dest_col in dest_row:
                        src_val = source_row[src_col]
                        dest_val = dest_row[dest_col]

                        if pd.isna(src_val) and pd.isna(dest_val):
                            continue  # Both are NaN → OK
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

            # Write mismatches to file
            with open("row_mismatches.txt", "w") as f:
                for line in mismatches:
                    f.write(line + "\n")
            
            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f"\nRow comparison complete. Mismatches found: {len(mismatches)}")
            print("See 'row_mismatches.txt' for details.")
            print(f"Time taken: {elapsed_time:.2f} seconds")
        except Exception as e:
            print(f"Error comparing rows: {e}")
