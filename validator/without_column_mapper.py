import pandas as pd
from file_read import FileReader

class WithoutColumnMapping:
    def __init__(self,src_path,dest_path,src_primary_key,dest_primary_key,threshold=0.8):
        self.src_path=src_path
        self.dest_path=dest_path
        self.threshold=threshold
        self.src_primary_key=src_primary_key
        self.dest_primary_key=dest_primary_key
        self.mapping={}

    def common_keys(self):
        common=set(self.src_df[self.src_primary_key]) & set (self.dest_df[self.dest_primary_key])
        #print(f"Found {len(common)} common keys")
        self.src_df=self.src_df[self.src_df[self.src_primary_key].isin(common)]
        self.dest_df=self.dest_df[self.dest_df[self.dest_primary_key].isin(common)]

        self.src_df.set_index(self.src_primary_key,inplace=True)
        self.dest_df.set_index(self.dest_primary_key,inplace=True)

        print(f"Loaded and aligned datasets on keys '{self.src_primary_key}' and '{self.dest_primary_key}'")

    def match_by_position(self):
        if self.src_df.shape[1]!=self.dest_df.shape[1]:
            print("Column counts mismatch")
            return False 

        src_cols=self.src_df.columns.tolist()
        dest_cols=self.dest_df.columns.tolist()

        print("\nComparing columns by position: ")

        for src_col,dest_col in zip(src_cols,dest_cols):
            match=self.src_df[src_col]==self.dest_df[dest_col]
            match_percent=sum(match)/len(self.src_df)
            if match_percent>=self.threshold:
                self.mapping[src_col]=dest_col 
            else:
                print(f"{src_col} vs {dest_col}: match={match_percent:.2f}-below threshold")

    def match_by_value(self):
        for src_col in self.src_df.columns:
            if src_col in self.mapping:
                continue 
                
            for dest_col in self.dest_df.columns:
                if dest_col in self.mapping.values():
                    continue

                match=self.src_df[src_col]==self.dest_df[dest_col]
                match_percent=sum(match)/len(self.src_df)
                if match_percent>=self.threshold and src_col not in self.mapping:
                    self.mapping[src_col]=dest_col
                    print(f"Matched by value: {src_col} -> {dest_col} (match: {match_percent:.2f})")


    def run(self):
        self.src_df=FileReader.read_csv(self.src_path)
        self.dest_df=FileReader.read_csv(self.dest_path)

        self.src_df = self.src_df.drop_duplicates(subset=self.src_primary_key, keep='first')
        self.dest_df = self.dest_df.drop_duplicates(subset=self.dest_primary_key, keep='first')

        print("\nSource PK unique:", self.src_df[self.src_primary_key].is_unique)
        print("Destination PK unique:", self.dest_df[self.dest_primary_key].is_unique)

        self.common_keys()

        self.match_by_position()
        
        self.match_by_value()


        print("\nInferred column mappings:")
        for src,dest in self.mapping.items():
            print(f"{src} - {dest}")



