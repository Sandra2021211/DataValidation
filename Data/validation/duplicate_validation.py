import pandas as pd
from file_reader import read_csv
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def check_duplicates(df, file_name):
    duplicates = df[df.duplicated()]
    count = len(duplicates)

    if count == 0:
        print(f"\nNo duplicate records found in {file_name}.")
    else:
        print(f"\nFound {count} duplicate records in {file_name}.")
        
        # print(duplicates)
    return count
