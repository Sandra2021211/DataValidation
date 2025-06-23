import pandas as pd
from itertools import combinations, product
from rapidfuzz import fuzz
import time

# Load Data
source_df = pd.read_csv("/workspaces/DataValidation/Data/src_data/insurance_claim.csv")
dest_df = pd.read_csv("/workspaces/DataValidation/Data/src_data/cleaned_insurance_claim_.csv")

start_time = time.time()

# 1. Key-finding Functions
def find_primary_keys(df):
    return [col for col in df.columns if df[col].is_unique]

def find_composite_key(df, max_combination=3):
    cols = df.columns
    for r in range(2, max_combination + 1):
        for combo in combinations(cols, r):
            if df.duplicated(subset=combo).sum() == 0:
                return list(combo)
    return None

def create_composite_index(df, cols):
    return df[cols].astype(str).agg('_'.join, axis=1)

# 2. Find matching key(s)
src_key = find_primary_keys(source_df)
dst_key = find_primary_keys(dest_df)

primary_key = None
for s_key, d_key in product(src_key, dst_key):
    if source_df[s_key].dtype == dest_df[d_key].dtype:
        overlap = set(source_df[s_key]) & set(dest_df[d_key])
        match_ratio = len(overlap) / min(len(source_df), len(dest_df))
        if match_ratio > 0.8:
            primary_key = ([s_key], [d_key])
            break

if not primary_key:
    src_comp = find_composite_key(source_df)
    dst_comp = find_composite_key(dest_df)
    if src_comp and dst_comp:
        source_df['composite_key'] = create_composite_index(source_df, src_comp)
        dest_df['composite_key'] = create_composite_index(dest_df, dst_comp)
        primary_key = (['composite_key'], ['composite_key'])
    else:
        raise Exception("No primary or composite key found with sufficient uniqueness.")

print(f"Using Key: {primary_key[0]} <--> {primary_key[1]}")

# 3. Align datasets
source_df.set_index(primary_key[0][0], inplace=True)
dest_df.set_index(primary_key[1][0], inplace=True)
common_index = source_df.index.intersection(dest_df.index)

source_aligned = source_df.loc[common_index].sort_index()
dest_aligned = dest_df.loc[common_index].sort_index()

# 4. Comparison Functions
def value_match_percentage(col1, col2):
    col1, col2 = col1.align(col2)
    match = (col1 == col2) | (col1.isna() & col2.isna())  # count NaNs as match
    return match.sum() / len(match) * 100

def string_similarity(col1, col2):
    col1, col2 = col1.align(col2)
    matches = 0
    for a, b in zip(col1, col2):
        if pd.isna(a) and pd.isna(b):
            matches += 1
        elif not pd.isna(a) and not pd.isna(b):
            if fuzz.ratio(str(a).strip(), str(b).strip()) > 80:
                matches += 1
    return matches / len(col1) * 100

# 5. Column-wise Comparison
best_matches = []

for src_col in source_aligned.columns:
    if src_col in primary_key[0]:
        continue
    for dest_col in dest_aligned.columns:
        if dest_col in primary_key[1]:
            continue
        try:
            if source_aligned[src_col].dtype == dest_aligned[dest_col].dtype:
                sim = value_match_percentage(source_aligned[src_col], dest_aligned[dest_col])
            else:
                sim = string_similarity(source_aligned[src_col], dest_aligned[dest_col])
            if sim >= 80:
                best_matches.append((src_col, dest_col, round(sim, 2)))
        except:
            continue  # skip if error

# 6. Filter Best Matches Only (per source column)
from collections import defaultdict
best_for_src = defaultdict(lambda: (None, None, 0))  # src_col: (dest_col, sim)

for src, dst, sim in best_matches:
    if sim > best_for_src[src][2]:
        best_for_src[src] = (dst, src, sim)

# 7. Output
end_time = time.time()
tot_time = (end_time - start_time) / 60
print(f"\nTotal time taken: {tot_time:.2f} minutes")

print("\nBest Matching Column Pairs (≥80% similarity):")
if best_for_src:
    for dst, src, sim in sorted(best_for_src.values(), key=lambda x: -x[2]):
        print(f"  {src} <--> {dst} : {sim}%")
else:
    print("  No column pairs with ≥80% match found.")
