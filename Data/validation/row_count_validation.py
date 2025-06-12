from file_reader import read_csv
import os
from dotenv import load_dotenv

load_dotenv()

def compare_row_and_column_counts(source_df, dest_df):
    #print(source_df.shape[0])
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