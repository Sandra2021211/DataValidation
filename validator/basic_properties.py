class BasicPropertiesValidator:
    def __init__(self, source_df, dest_df, column_mappings):
        self.source_df = source_df
        self.dest_df = dest_df
        self.column_mappings = column_mappings

#Comparing row counts between source and desination
    def compare_row_count(self):
        print("\nRow Count Comparison:")
        a = len(self.source_df)
        b = len(self.dest_df)
        print(f"Source dataset: {a}, Destination dataset: {b}")
        if a == b:
            print("Row counts match")
        else:
            print("Row counts do not match")

#Validate data types consistency after mapping
    def validate_data_types(self):
        mismatch = []
        for src, dest in self.column_mappings.items():
            if src in self.source_df.columns and dest in self.dest_df.columns:
                a = str(self.source_df[src].dtype)
                b = str(self.dest_df[dest].dtype)
                if a != b:
                    mismatch.append((src, dest, a, b))

        print("\nData Type Validation:")
        if mismatch:
            print("Mismatch found:")
            for s_data, dest_data, a_data, b_data in mismatch:
                print(f"{s_data} is of datatype {a_data} and {dest_data} is of datatype {b_data}")
        else:
            print("Data types match after mapping")

#Check for duplicate records in both datasets
    def check_duplicate(self, df, label):
        print(f"\nDuplicate Check - {label}:")
        if df.duplicated().any():
            print(f"Duplicate rows found in {label}")
            print(df[df.duplicated()])
        else:
            print(f"No duplicates in {label}")

#Identify completely empty rows
    def check_empty_rows(self, df, label):
        print(f"\nEmpty Row Check - {label}:")
        empty_rows = df[df.isnull().all(axis=1)]
        if not empty_rows.empty:
            print(f"Empty rows found in {label}: {len(empty_rows)}")
        else:
            print(f"No completely empty rows in {label}")
