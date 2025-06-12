import pandas as pd
import os
from dotenv import load_dotenv
from file_reader import read_csv

load_dotenv()

def validate_data_types(src_df, dest_df, col_mappings):
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