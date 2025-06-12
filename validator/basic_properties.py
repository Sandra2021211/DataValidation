import pandas as pd
import json 

#Reading csv file
def read_csv(path):
    return pd.read_csv(path)

#Reading json file
def read_json(path):
    with open(path) as f:
        return json.load(f)

#Comparing row counts between source and desination
def compare_row_count(src_df,dest_df):
    a=len(src_df)
    b=len(dest_df)
    print("\nRow count: ")
    print(f"Source dataset: {a}, Destination dataset: {b}")
    if a==b:
        print("Row counts match")
    else:
        print("Row counts do not match")

#Validate data types consistency after mapping
def validate_data_types(src_df,dest_df,col_mappings):
    mismatch=[]
    for src,dest in col_mappings.items():
        if src in src_df.columns and dest in dest_df.columns:
            a=str(src_df[src].dtype)
            b=str(dest_df[dest].dtype)
            if a!=b:
                mismatch.append((src,dest,a,b))

    print("\nData Type Validation:")
    if mismatch:
        print("Mismatch found:")
        for s_data,dest_data,a_data,b_data in mismatch:
            print(f"{s_data} is of datatype {a_data} and {dest_data} is of datatype {b_data}")
    
    else:
        print("Data types match after mapping")

#Check for duplicate records in both datasets
def check_duplicate(df,label):
    print(f"\nDuplicate check-{label}:")
    if df.duplicated().any():
        print(f"Duplicate rows found in {label}")
        print(df[df.duplicated()])
    else:
        print(f"No duplicates found in {label}")

#Identify completely empty rows
def check_emptyrows(df,label):
    print(f"\nCheck empty rows in {label}:")
    empty_rows=df[df.isnull().all(axis=1)]
    if not empty_rows.empty:
        print(f"Empty rows found in {label}: {len(empty_rows)}")
    else:
        print(f"No completely empty rows in {label}")


if __name__ == '__main__':
    src_path="src_data/insurance_claims.csv"
    dest_path="src_data/cleaned_insurance_claims.csv"
    map_path="src_data/mapping.json"

    src_df=read_csv(src_path)
    dest_df=read_csv(dest_path)
    mapping=read_json(map_path)
    col_mappings=mapping['column_mappings']

    print("Basic dataset properties:")
    compare_row_count(src_df,dest_df)
    validate_data_types(src_df,dest_df,col_mappings)
    check_duplicate(src_df,"Source Dataset")
    check_duplicate(dest_df,"Destination Dataset")
    check_emptyrows(src_df,"Source Dataset")
    check_emptyrows(dest_df,"Destination Dataset")
