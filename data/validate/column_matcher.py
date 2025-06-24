import pandas as pd
from file_read import FileReader

class ColumnMatcher:
    def __init__(self, source_path, destination_path, source_key, destination_key, match_threshold=0.8):
        self.source_path = source_path
        self.destination_path = destination_path
        self.match_threshold = match_threshold  
        self.source_key = source_key
        self.destination_key = destination_key
        self.column_mapping = {} 

    def align_common_keys(self):
    
        common_keys = set(self.source_df[self.source_key]) & set(self.destination_df[self.destination_key])

        if not common_keys:
            raise ValueError(f"No common keys found between '{self.source_key}' and '{self.destination_key}'.")

        # Filter rows 
        self.source_df = self.source_df[self.source_df[self.source_key].isin(common_keys)].copy()
        self.destination_df = self.destination_df[self.destination_df[self.destination_key].isin(common_keys)].copy()

        # Reset indices after filtering
        self.source_df = self.source_df.set_index(self.source_key)
        self.destination_df = self.destination_df.set_index(self.destination_key)

        # Ensure identical indices 
        self.source_df = self.source_df.loc[self.destination_df.index]
        print(f"Aligned datasets using keys '{self.source_key}' and '{self.destination_key}'")

    def match_columns_by_position(self):
        if self.source_df.shape[1] != self.destination_df.shape[1]:
            print("Column counts mismatch")
            return False

        source_columns = self.source_df.columns.tolist()
        destination_columns = self.destination_df.columns.tolist()

        print("\nComparing columns by position:")
        for src_col, dest_col in zip(source_columns, destination_columns):
            try:
                # Numeric comparison
                source_series = pd.to_numeric(self.source_df[src_col], errors='coerce')
                destination_series = pd.to_numeric(self.destination_df[dest_col], errors='coerce')

                if source_series.notna().sum() > 0 and destination_series.notna().sum() > 0:
                    match = (source_series.fillna(0).astype(int) == destination_series.fillna(0).astype(int))
                else:
                    raise ValueError
            except:
                # String comparison
                source_series = self.source_df[src_col].fillna('').astype(str).str.strip()
                destination_series = self.destination_df[dest_col].fillna('').astype(str).str.strip()
                match = source_series == destination_series

            match_percentage = sum(match) / len(self.source_df)
            if match_percentage >= self.match_threshold:
                self.column_mapping[src_col] = dest_col
                print(f"Matched by position: {src_col} -> {dest_col} (match: {match_percentage:.2f})")
            else:
                print(f"{src_col} vs {dest_col}: match={match_percentage:.2f} - below threshold")

    def match_columns_by_value(self):
        for src_col in self.source_df.columns:
            if src_col in self.column_mapping:
                continue

            for dest_col in self.destination_df.columns:
                if dest_col in self.column_mapping.values():
                    continue

                try:
                    # Numeric comparison
                    source_series = pd.to_numeric(self.source_df[src_col], errors='coerce')
                    destination_series = pd.to_numeric(self.destination_df[dest_col], errors='coerce')

                    if source_series.notna().sum() > 0 and destination_series.notna().sum() > 0:
                        match = (source_series.fillna(0).astype(int) == destination_series.fillna(0).astype(int))
                    else:
                        raise ValueError
                except:
                    # String comparison
                    source_series = self.source_df[src_col].fillna('').astype(str).str.strip()
                    destination_series = self.destination_df[dest_col].fillna('').astype(str).str.strip()
                    match = source_series == destination_series

                match_percentage = sum(match) / len(self.source_df)
                if match_percentage >= self.match_threshold and src_col not in self.column_mapping:
                    self.column_mapping[src_col] = dest_col
                    print(f"Matched by value: {src_col} -> {dest_col} (match: {match_percentage:.2f})")

    def execute(self):

        self.source_df = FileReader.read_csv(self.source_path)
        self.destination_df = FileReader.read_csv(self.destination_path)

        # Drop duplicates based on primary key
        self.source_df = self.source_df.drop_duplicates(subset=self.source_key, keep='first')
        self.destination_df = self.destination_df.drop_duplicates(subset=self.destination_key, keep='first')

        print("\nSource dataset columns:", self.source_df.columns.tolist())
        print("Destination dataset columns:", self.destination_df.columns.tolist())

        print("\nSource PK unique:", self.source_df[self.source_key].is_unique)
        print("Destination PK unique:", self.destination_df[self.destination_key].is_unique)

        # Align datasets by common primary keys
        self.align_common_keys()

        # Match columns by their position
        self.match_columns_by_position()

        # Match remaining columns by value
        self.match_columns_by_value()
        print("\nFinal column mappings")
        for src, dest in self.column_mapping.items():
            print(f"{src} -> {dest}")
