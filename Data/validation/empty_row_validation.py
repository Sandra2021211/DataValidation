import pandas as pd
from dotenv import load_dotenv
import os
from file_reader import read_csv

load_dotenv()

def check_empty_rows(df, file_name):
    # Identify fully empty rows
    empty_rows = df[df.isnull().all(axis=1)]
    count = len(empty_rows)

    print(f"\nChecking completely empty rows in {file_name} dataset:")
    if count == 0:
        print(f"No completely empty rows found in {file_name}.")
    else:
        print(f"Found {count} completely empty rows in {file_name}.")
        # print(empty_rows)
    return count