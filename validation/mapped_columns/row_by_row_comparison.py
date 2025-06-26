import pandas as pd
import time
from multiprocessing import Pool, cpu_count
import traceback

def compare_row_multiprocess(args):
    try:
        k, source_dict, dest_dict, col_mappings = args
        mismatch = []

        src_row = source_dict.get(k)
        dest_row = dest_dict.get(k)

        if dest_row is None:
            mismatch.append((k, "row", "missing in destination"))
            return mismatch

        for src_col, dest_col in col_mappings.items():
            # Use get to avoid KeyError
            src_val = src_row.get(src_col)
            dest_val = dest_row.get(dest_col)

            if pd.isnull(src_val) and pd.isnull(dest_val):
                continue

            if src_val != dest_val:
                mismatch.append((k, src_col, dest_col, src_val, dest_val))

        return mismatch

    except Exception as e:
        print(f"Error comparing row {k}: {type(e).__name__}: {e}")
        traceback.print_exc()
        return [(k, "error", str(e))]


class RowByRowComparator:
    def __init__(self, source_df, dest_df, col_mappings, src_primary_key, dest_primary_key):
        try:
            self.source_df = source_df.copy()
            self.dest_df = dest_df.copy()
            self.col_mappings = col_mappings
            self.src_primary_key = src_primary_key
            self.dest_primary_key = dest_primary_key

            self.source_df.set_index(src_primary_key, inplace=True)
            self.dest_df.set_index(dest_primary_key, inplace=True)

            self.source_dict = self.source_df.to_dict(orient="index")
            self.dest_dict = self.dest_df.to_dict(orient="index")

        except KeyError as e:
            print(f"KeyError during initialization: Missing primary key column: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error during initialization: {type(e).__name__}: {e}")
            raise

    def compare(self):
        print("\nRow by Row comparison:")
        start_time = time.time()

        try:
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

        except Exception as e:
            print(f"Error during row-by-row comparison: {type(e).__name__}: {e}")
            traceback.print_exc()

        end_time = time.time()
        print(f"Time taken for row-by-row comparison: {end_time - start_time:.2f} seconds")
