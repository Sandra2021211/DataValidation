class BasicPropertiesValidator:
    def __init__(self, source_df, dest_df, mapping_data):
        self.source_df = source_df
        self.dest_df = dest_df
        self.mapping_data = mapping_data

    # to check the completely empty rows
    def check_empty_rows(self, df, file_name):
        # Identify fully empty rows
        empty_rows = df[df.isnull().all(axis=1)]
        count = len(empty_rows)

        print(f"\nChecking completely empty rows in {file_name} dataset:")
        if count == 0:
            print(f"No completely empty rows found in {file_name}.")
        else:
            print(f"Found {count} completely empty rows in {file_name}.")
        return count

    # to check the duplicate rows
    def check_duplicates(self, df, file_name):
        duplicates = df[df.duplicated()]
        count = len(duplicates)

        if count == 0:
            print(f"\nNo duplicate records found in {file_name}.")
        else:
            print(f"\nFound {count} duplicate records in {file_name}.")
        return count

    # to check the datatype validation
    def validate_data_types(self, src_df, dest_df, col_mappings):
        mismatch = []
        for src, dest in col_mappings.items():
            if src in src_df.columns and dest in dest_df.columns:
                src_dtype = str(src_df[src].dtype)
                dest_dtype = str(dest_df[dest].dtype)

                if src_dtype != dest_dtype:
                    mismatch.append((src, dest, src_dtype, dest_dtype))

        print("\nData Type Validation:")

        if mismatch:
            print("Mismatch found:")
            for src_col, dest_col, src_type, dest_type in mismatch:
                print(f"{src_col} is of type {src_type}, but {dest_col} is of type {dest_type}")
        else:
            print("All column data types match.")

    # to compare the row and column counts
    def compare_row_and_column_counts(self, source_df, dest_df):
        source_rows, source_cols = source_df.shape
        dest_rows, dest_cols = dest_df.shape

        print("\n----Row and Column Count Comparison----")
        print(f" Source:      {source_rows} rows × {source_cols} columns")
        print(f" Destination: {dest_rows} rows × {dest_cols} columns")

        if source_rows == dest_rows:
            print("Row count matches.")
        else:
            diff = abs(source_rows - dest_rows)
            print(f" Row count mismatch! Difference: {diff} rows.")

        if source_cols == dest_cols:
            print("Column count matches.")
        else:
            diff = abs(source_cols - dest_cols)
            print(f"Column count mismatch! Difference: {diff} columns.")
