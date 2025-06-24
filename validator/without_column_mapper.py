import pandas as pd
from file_read import FileReader

class WithoutColumnMapping:
    def __init__(self,src_path,dest_path,src_primary_key,dest_primary_key,threshold=0.8):
        self.src_path=src_path
        self.dest_path=dest_path
        self.threshold=threshold # matching threshold- 80%
        self.src_primary_key=src_primary_key
        self.dest_primary_key=dest_primary_key
        self.mapping={} # Holds the final matched column pairs

    def common_keys(self):
        # identify common primary key values in both datasets
        common=set(self.src_df[self.src_primary_key]) & set (self.dest_df[self.dest_primary_key])
        #print(f"Found {len(common)} common keys")

        # Filter rows to keep only matching primary keys
        self.src_df=self.src_df[self.src_df[self.src_primary_key].isin(common)]
        self.dest_df=self.dest_df[self.dest_df[self.dest_primary_key].isin(common)]

        # setting primary key as the index
        self.src_df.set_index(self.src_primary_key,inplace=True)
        self.dest_df.set_index(self.dest_primary_key,inplace=True)

        print(f"Loaded and aligned datasets on keys '{self.src_primary_key}' and '{self.dest_primary_key}'")

    def match_by_position(self):
        if self.src_df.shape[1]!=self.dest_df.shape[1]:
            print("Column counts mismatch")
            return False 

        # Get column names in order as lists
        src_cols=self.src_df.columns.tolist()
        dest_cols=self.dest_df.columns.tolist()

        print("\nComparing columns by position: ")

        for src_col,dest_col in zip(src_cols,dest_cols):

            try:
                # for numeric mismatches
                src_series=pd.to_numeric(self.src_df[src_col],errors='coerce')
                dest_series=pd.to_numeric(self.dest_df[dest_col],errors='coerce')

                if src_series.notna().sum()>0 and dest_series.notna().sum()>0:
                    match=(src_series.fillna(0).astype(int)==dest_series.fillna(0).astype(int)) # replaces NaN with 0 and converts the float to int
                else:
                    raise ValueError

            except:
                # Clean and normalize both columns (fill missing values, convert to string, strip spaces)
                src_series=self.src_df[src_col].fillna('').astype(str).str.strip()
                dest_series=self.dest_df[dest_col].fillna('').astype(str).str.strip()

                #match=self.src_df[src_col]==self.dest_df[dest_col]
                # Perform row wise comparison
                match= src_series==dest_series

            # Calculate match percentage
            match_percent=sum(match)/len(self.src_df)

            if match_percent>=self.threshold:
                self.mapping[src_col]=dest_col  # Store matched pair
                print(f"Matched by position: {src_col} -> {dest_col} (match: {match_percent:.2f})")
            else:
                print(f"{src_col} vs {dest_col}: match={match_percent:.2f}-below threshold")

    def match_by_value(self):
         # Compare every unmatched source column to every unmatched destination column
        for src_col in self.src_df.columns:
            if src_col in self.mapping:
                continue 
                
            for dest_col in self.dest_df.columns:
                if dest_col in self.mapping.values():
                    continue

                try:
                    # for numeric mismatches
                    src_series=pd.to_numeric(self.src_df[src_col],errors='coerce')
                    dest_series=pd.to_numeric(self.dest_df[dest_col],errors='coerce')

                    if src_series.notna().sum()>0 and dest_series.notna().sum()>0:
                        #match=(abs(src_series-dest_series)<0.01)
                        match=(src_series.fillna(0).astype(int)==dest_series.fillna(0).astype(int)) # replaces NaN with 0 and converts the float to int
                    else:
                        raise ValueError

                except:
                    src_series=self.src_df[src_col].fillna('').astype(str).str.strip()
                    dest_series=self.dest_df[dest_col].fillna('').astype(str).str.strip()

                    # Row wise comparison
                    match=src_series==dest_series

                match_percent=sum(match)/len(self.src_df)
                if match_percent>=self.threshold and src_col not in self.mapping:
                    self.mapping[src_col]=dest_col
                    print(f"Matched by value: {src_col} -> {dest_col} (match: {match_percent:.2f})")
                #else:
                    #print(f"{src_col} vs {dest_col}: match={match_percent:.2f}-below threshold")


    def run(self):
        self.src_df=FileReader.read_csv(self.src_path)
        self.dest_df=FileReader.read_csv(self.dest_path)

        # Drop duplicate records based on the primary key column
        self.src_df = self.src_df.drop_duplicates(subset=self.src_primary_key, keep='first')
        self.dest_df = self.dest_df.drop_duplicates(subset=self.dest_primary_key, keep='first')

        print("\nSource PK unique:", self.src_df[self.src_primary_key].is_unique)
        print("Destination PK unique:", self.dest_df[self.dest_primary_key].is_unique)

        # Step 1: Align by common primary keys
        self.common_keys()

        # Step 2: Try matching columns by their position
        self.match_by_position()

        # Step 3: Fallback - Try matching remaining columns by value similarity        
        self.match_by_value()

        # Final mapping result
        print("\nInferred column mappings:")
        for src,dest in self.mapping.items():
            print(f"{src} - {dest}")



