import pandas as pd
import yaml
import json

class StreamingData:
    def __init__(self, src_df, dest_df):
        self.src_df = src_df
        self.dest_df = dest_df

    def corrupted_dateframe(self, start, end):
        c_start = pd.to_datetime(start)
        c_end = pd.to_datetime(end)

        #self.src_df['stream_time'] = pd.to_datetime(self.src_df['stream_time'])
        #self.dest_df['stream_time'] = pd.to_datetime(self.dest_df['stream_time'])

        src_window = self.src_df[(self.src_df['stream_time'] >= c_start) & (self.src_df['stream_time'] <= c_end)]
        dest_window = self.dest_df[(self.dest_df['stream_time'] >= c_start) & (self.dest_df['stream_time'] <= c_end)]

        return src_window, dest_window


class RowByRowComparator:
    def __init__(self, source_df, dest_df, col_mappings, src_primary_key, dest_primary_key):
        self.source_df = source_df.copy()
        self.dest_df = dest_df.copy()
        self.col_mappings = col_mappings
        self.src_primary_key = src_primary_key
        self.dest_primary_key = dest_primary_key

        self.source_df.set_index(src_primary_key, inplace=True)
        self.dest_df.set_index(dest_primary_key, inplace=True)

    def compare(self):
        print("\n🔍 Row by Row comparison:")
        mismatch = []

        for k in self.source_df.index:
            if k not in self.dest_df.index:
                mismatch.append((k, "row", "missing in destination"))
                continue

            src_row = self.source_df.loc[k]
            dest_row = self.dest_df.loc[k]

            for src_col, dest_col in self.col_mappings.items():
                if src_col in src_row and dest_col in dest_row:
                    src_val = src_row[src_col]
                    dest_val = dest_row[dest_col]

                    if pd.isnull(src_val) and pd.isnull(dest_val):
                        continue

                    elif str(src_val) != str(dest_val):
                        mismatch.append((k, src_col, dest_col, src_val, dest_val))

        if mismatch:
            print("❌ Mismatches found:")
            for mis in mismatch:
                if len(mis) == 3:
                    print(f"Row {mis[0]}: {mis[2]}")
                else:
                    print(f"Row {mis[0]} | Source: {mis[1]} → {mis[3]} , Destination: {mis[2]} → {mis[4]}")
        else:
            print("✅ All rows match!")


def main():
    # File paths
    test_src = "src_data/s.csv"
    test_dest = "src_data/d.csv"
    map_path = "src_data/map.json"
    yaml_path = "src_data/requirement.yaml"

    # Load files
    test_src_df = pd.read_csv(test_src)
    test_dest_df = pd.read_csv(test_dest)

    with open(map_path, 'r') as fi:
        mapping = json.load(fi)

    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)

    col_mappings = mapping["column_mappings"]
    src_primary_key = "CLM_ID"
    dest_primary_key = "claim_id"

    print("🔹 Sample Destination Row:", test_dest_df.iloc[0])
    print("🔹 Sample Source Row:", test_src_df.iloc[0])

    # Get corrupted date window
    stream = StreamingData(test_src_df, test_dest_df)
    start_date = config["validation_config"]["date_filter"]["start_date"]
    end_date = config["validation_config"]["date_filter"]["end_date"]

    src_window, dest_window = stream.corrupted_dateframe(start_date, end_date)

    src_window = src_window.drop_duplicates(subset=src_primary_key, keep='first')
    dest_window = dest_window.drop_duplicates(subset=dest_primary_key, keep='first')

    print(f"\n🗓 Comparing 1-week window: {start_date} to {end_date}")

    # Column filtering mode
    mode = config["validation_config"]["column_comparison"]["mode"]
    if mode == "specific":
        selected_cols = config["validation_config"]["column_comparison"]["columns"]
        c_map = {k: v for k, v in col_mappings.items() if k in selected_cols}
    else:
        c_map = col_mappings

    # Perform comparison
    window_comparator = RowByRowComparator(src_window, dest_window, c_map, src_primary_key, dest_primary_key)
    window_comparator.compare()


if __name__ == "__main__":
    main()
