import pandas as pd
from difflib import SequenceMatcher
from itertools import combinations, product
import time

source_data = pd.read_csv("/workspaces/DataValidation/data/src_data/insurance_Claim_.csv")
destination_data = pd.read_csv("/workspaces/DataValidation/data/src_data/cleaned_insurance_claim_.csv")

start_time = time.time()

def identify_primary_keys(dataframe):
    return [column for column in dataframe.columns if dataframe[column].is_unique]

def identify_composite_keys(dataframe, max_combination=3):
    columns = dataframe.columns
    for r in range(2, max_combination + 1):
        for combo in combinations(columns, r):
            if dataframe.duplicated(subset=combo).sum() == 0:
                return list(combo)
    return None

def generate_composite_index(dataframe, columns):
    return dataframe[columns].astype(str).agg('_'.join, axis=1)

# Find possible single primary keys
source_primary_keys = identify_primary_keys(source_data)
destination_primary_keys = identify_primary_keys(destination_data)

# Check if there's a matching primary key
primary_key_pair = None
for source_key, destination_key in product(source_primary_keys, destination_primary_keys):
    if source_data[source_key].dtype == destination_data[destination_key].dtype:
        common_values = set(source_data[source_key]) & set(destination_data[destination_key])
        match_ratio = len(common_values) / min(len(source_data), len(destination_data))
        if match_ratio > 0.8:
            primary_key_pair = ([source_key], [destination_key])
            break

# If no single key found, check for composite key
if not primary_key_pair:
    source_composite_key = identify_composite_keys(source_data)
    destination_composite_key = identify_composite_keys(destination_data)
    if source_composite_key and destination_composite_key:
        source_data['composite_key'] = generate_composite_index(source_data, source_composite_key)
        destination_data['composite_key'] = generate_composite_index(destination_data, destination_composite_key)
        primary_key_pair = (['composite_key'], ['composite_key'])
    else:
        raise Exception("No primary or composite key found with sufficient uniqueness.")

print(f"Using Key: {primary_key_pair[0]} <-> {primary_key_pair[1]}")

# Align rows by primary key
source_data.set_index(primary_key_pair[0][0], inplace=True)
destination_data.set_index(primary_key_pair[1][0], inplace=True)
common_indices = source_data.index.intersection(destination_data.index)

aligned_source_data = source_data.loc[common_indices]
aligned_destination_data = destination_data.loc[common_indices]

# Compare columns for similarity
def calculate_value_match_percentage(column1, column2):
    matches = (column1 == column2)
    return matches.sum() / len(matches) * 100

def calculate_string_similarity(column1, column2):
    matches = sum(
        SequenceMatcher(None, str(a), str(b)).ratio() > 0.8
        for a, b in zip(column1, column2)
    )
    return matches / len(column1) * 100

# Find best-matching column pairs
column_matches = []

for source_column in aligned_source_data.columns:
    for destination_column in aligned_destination_data.columns:
        if source_column in primary_key_pair[0] or destination_column in primary_key_pair[1]:
            continue 
        try:
            if aligned_source_data[source_column].dtype == aligned_destination_data[destination_column].dtype:
                similarity = calculate_value_match_percentage(aligned_source_data[source_column], aligned_destination_data[destination_column])
            else:
                similarity = calculate_string_similarity(aligned_source_data[source_column].astype(str), aligned_destination_data[destination_column].astype(str))
            if similarity >= 80:
                column_matches.append((source_column, destination_column, round(similarity, 2)))
        except:
            continue 

column_matches.sort(key=lambda x: -x[2])

end_time = time.time()
tot_time = (end_time-start_time)/60
print(f"Total time taken :{tot_time:.2f} minutes")

print("\nBest Matching Column Pairs (>=80% similarity):")
if column_matches:
    for src_col, dest_col, similarity_score in column_matches:
        print(f"  {src_col} <-> {dest_col} : {similarity_score}%")
else:
    print("  No column pairs with ≥80% match found.")
