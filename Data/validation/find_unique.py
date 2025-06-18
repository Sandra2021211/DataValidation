import pandas as pd
import itertools

df = pd.read_csv("/workspaces/DataValidation/Data/src_data/insurance_claim.csv")

# Drop fully identical rows
df = df.drop_duplicates()

# Function to find the smallest combination of columns that forms a unique key 
def find_min_unique_key(df):
    cols = df.columns.tolist()
    for r in range(1, len(cols) + 1):
        for combo in itertools.combinations(cols, r):
            if df.duplicated(subset=combo).sum() == 0:
                return combo
    return None

# Find unique key columns
unique_key_columns = find_min_unique_key(df)

# Display results
if unique_key_columns:
    print("Smallest unique key combination found:")
    print(f"Columns used: {unique_key_columns}\n")
else:
    print(" No unique key combination found.")