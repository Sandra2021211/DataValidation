import pandas as pd
import time
import yaml
from multiprocessing import Pool, cpu_count


def compare_row_multiprocess(args):
    k, source_dict, dest_dict, col_mappings = args
    mismatch = []

    src_row = source_dict.get(k)
    dest_row = dest_dict.get(k)

    if dest_row is None:
        mismatch.append((k, "row", "missing in destination"))
        return mismatch

    for src_col, dest_col in col_mappings.items():
        src_val = src_row.get(src_col)
        dest_val = dest_row.get(dest_col)

        if pd.isnull(src_val) and pd.isnull(dest_val):
            continue

        if src_val != dest_val:
            mismatch.append((k, src_col, dest_col, src_val, dest_val))
    return mismatch


class RowByRowComparator:
    def __init__(self, source_df, dest_df, col_mappings, src_primary_key, dest_primary_key):
        self.source_df = source_df.copy()
        self.dest_df = dest_df.copy()
        self.col_mappings = col_mappings
        self.src_primary_key = src_primary_key
        self.dest_primary_key = dest_primary_key

        self.source_df.set_index(src_primary_key, inplace=True)
        self.dest_df.set_index(dest_primary_key, inplace=True)

        self.source_dict = self.source_df.to_dict(orient="index")
        self.dest_dict = self.dest_df.to_dict(orient="index")

    def compare(self):
        print("\nRow by Row comparison:")
        start_time = time.time()

        keys = list(self.source_dict.keys())
        input_data = [(k, self.source_dict, self.dest_dict, self.col_mappings) for k in keys]

        with Pool(processes=cpu_count()) as pool:
            results = pool.map(compare_row_multiprocess, input_data)

        all_mismatch = [m for sublist in results for m in sublist if sublist]

        if all_mismatch:
            print("Mismatches found:")
            for mis in all_mismatch:
                if len(mis) == 3:
                    print(f"Row {mis[0]}: {mis[2]}")
                else:
                    print(f"Row {mis[0]} | Source: {mis[1]}-{mis[3]} , Destination: {mis[2]}-{mis[4]}")
        else:
            print("All rows match!!!")

        end_time = time.time()
        print(f"Time taken for row-by-row comparison: {end_time - start_time:.2f} seconds")


class CustomDatasetValidator:
    def __init__(self, src_path, dest_path, map_path, yaml_path):
        self.src_path = src_path
        self.dest_path = dest_path
        self.map_path = map_path
        self.yaml_path = yaml_path

    def corrupted_dateframe(self, src_df, dest_df, start, end):
        c_start = pd.to_datetime(start)
        c_end = pd.to_datetime(end)

        src_window = src_df[(src_df['stream_time'] >= c_start) & (src_df['stream_time'] <= c_end)]
        dest_window = dest_df[(dest_df['stream_time'] >= c_start) & (dest_df['stream_time'] <= c_end)]

        return src_window, dest_window

    def run(self):
        test_src_df = pd.read_csv(self.src_path, parse_dates=['stream_time'])
        test_dest_df = pd.read_csv(self.dest_path, parse_dates=['stream_time'])
        mapping = pd.read_json(self.map_path)

        with open(self.yaml_path, 'r') as f:
            config = yaml.safe_load(f)

        col_mappings = mapping["column_mappings"]
        src_primary_key = "CLM_ID"
        dest_primary_key = "claim_id"

        start_date = config["validation_config"]["date_filter"]["start_date"]
        end_date = config["validation_config"]["date_filter"]["end_date"]

        src_window, dest_window = self.corrupted_dateframe(test_src_df, test_dest_df, start_date, end_date)

        src_window = src_window.drop_duplicates(subset=src_primary_key, keep='first')
        dest_window = dest_window.drop_duplicates(subset=dest_primary_key, keep='first')

        print(f"\n🗓 Comparing 1-week window: {start_date} to {end_date}")

        mode = config["validation_config"]["column_comparison"]["mode"]
        if mode == "specific":
            selected_cols = config["validation_config"]["column_comparison"]["columns"]
            c_map = {k: v for k, v in col_mappings.items() if v in selected_cols}
        else:
            c_map = col_mappings

        print("Column mappings used for comparison:\n", c_map)

        window_comparator = RowByRowComparator(src_window, dest_window, c_map, src_primary_key, dest_primary_key)
        window_comparator.compare()