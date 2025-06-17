import pandas as pd
import json

# Function to add dates for a time period of two months to the data frames
def add_date(source_df, destination_df, start_date, end_date):
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    date_range = pd.date_range(start=start, end=end, periods=len(source_df))
    source_df['stream_time'] = date_range
    destination_df['stream_time'] = date_range.copy()

# Function to extract a one-week window of corrupted data
def corrupted_dateframe(source_df, destination_df, start, end):
    c_start = pd.to_datetime(start)
    c_end = pd.to_datetime(end)

    source_window = source_df[
        (source_df['stream_time'] >= c_start) & (source_df['stream_time'] <= c_end)
    ]
    destination_window = destination_df[
        (destination_df['stream_time'] >= c_start) & (destination_df['stream_time'] <= c_end)
    ]

    return source_window, destination_window

# Function to compare rows by claim ID
def compare_rows_by_claim_id(source_df, destination_df, mapping_data):
    column_mappings = mapping_data["column_mappings"]
    primary_key = mapping_data["validation_rules"]["primary_key"]

    source_key = None
    for src_col, dest_col in column_mappings.items():
        if dest_col == primary_key:
            source_key = src_col
            break

    if source_key is None:
        print("Could not find source primary key for the destination primary key.")
        return
    if primary_key not in destination_df.columns or source_key not in source_df.columns:
        print("Primary key column is missing in one of the datasets.")
        return

    mismatches = []

    for _, dest_row in destination_df.iterrows():
        claim_id = dest_row[primary_key]

        source_row = source_df[source_df[source_key] == claim_id]

        if source_row.empty:
            mismatches.append(f"Destination claim_id '{claim_id}' not found in source.\n")
            continue

        source_row = source_row.iloc[0]

        for src_col, dest_col in column_mappings.items():
            if src_col in source_row and dest_col in dest_row:
                src_val = source_row[src_col]
                dest_val = dest_row[dest_col]

                if pd.isna(src_val) and pd.isna(dest_val):
                    continue  # both are NaN → OK
                elif pd.isna(src_val) != pd.isna(dest_val) or str(src_val) != str(dest_val):
                    mismatches.append(
                        f"ID {claim_id}: {src_col} -> {dest_col} mismatch: source='{src_val}' destination='{dest_val}'"
                    )

    with open("mismatches.txt", "w") as f:
        for line in mismatches:
            f.write(line + "\n")

    print(f"Total mismatches found: {len(mismatches)}")

# Main execution block
if __name__ == "__main__":
    with open("/workspaces/DataValidation/data/src_data/insurance_mapping.json") as f:
        mapping_data = json.load(f)

    src_df = pd.read_csv("/workspaces/DataValidation/data/src_data/expanded_source.csv")
    dst_df = pd.read_csv("/workspaces/DataValidation/data/src_data/expanded_destination.csv")

    # Adding stream_time columns
    add_date(src_df, dst_df, "2023-01-01", "2023-02-28")

    # Identifying corrupted data
    source_window, destination_window = corrupted_dateframe(src_df, dst_df, "2023-01-15", "2023-01-22")
    print("Corrupted data window extracted.")

    # Comparing rows by claim ID
    compare_rows_by_claim_id(source_window, destination_window, mapping_data)
