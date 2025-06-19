import pandas as pd 
from file_read import FileReader
from row_by_row_comparison import RowByRowComparator 
import sys 

class CustomDatasetValidator:
    def __init__(self, src_path, dest_path, map_path, yaml_path):
        self.src_path = src_path
        self.dest_path = dest_path
        self.map_path = map_path
        self.yaml_path = yaml_path

    def corrupted_dateframe(self,src_df,dest_df,start,end):
        c_start = pd.to_datetime(start)
        c_end = pd.to_datetime(end)

        #self.src_df['stream_time'] = pd.to_datetime(self.src_df['stream_time'])
        #self.dest_df['stream_time'] = pd.to_datetime(self.dest_df['stream_time'])

        #print("Source stream_time range:", self.src_df['stream_time'].min(), "to", self.src_df['stream_time'].max())
        #print("Dest stream_time range:", self.dest_df['stream_time'].min(), "to", self.dest_df['stream_time'].max())


        src_window = src_df[(src_df['stream_time'] >= c_start) & (src_df['stream_time'] <= c_end)]
        dest_window = dest_df[(dest_df['stream_time'] >= c_start) & (dest_df['stream_time'] <= c_end)]

        #print("Source window size:", len(src_window))
        #print("Destination window size:", len(dest_window))


        return src_window, dest_window

    def run(self):
        try:
            # Read files
            test_src_df = FileReader.read_csv(self.src_path, parse_dates=['stream_time'])
            test_dest_df = FileReader.read_csv(self.dest_path, parse_dates=['stream_time'])
            mapping = FileReader.read_json(self.map_path)
            config = FileReader.read_yaml(self.yaml_path)

            if "column_mappings" not in mapping:
                    raise KeyError("Missing 'column_mappings' in mapping.json")

            col_mappings = mapping["column_mappings"]
            src_primary_key = "CLM_ID"
            dest_primary_key = "claim_id"

            #print("Source datatypes:",test_src_df.dtypes)
            #print("Destination datatypes:",test_dest_df.dtypes)

            #print("Sample Destination Row:", test_dest_df.iloc[0])
            #print("Sample Source Row:", test_src_df.iloc[0])

            # Get corrupted date window
            start_date = config["validation_config"]["date_filter"]["start_date"]
            end_date = config["validation_config"]["date_filter"]["end_date"]

            src_window, dest_window = self.corrupted_dateframe(test_src_df,test_dest_df,start_date, end_date)

            #print("Rows in filtered source:", len(src_window))
            #print("Rows in filtered destination:", len(dest_window))

            #print("Destination filtered preview:\n", dest_window[[dest_primary_key, 'stream_time']])
            #print("Source filtered preview:\n", src_window[[src_primary_key, 'stream_time']])

            src_window = src_window.drop_duplicates(subset=src_primary_key, keep='first')
            dest_window = dest_window.drop_duplicates(subset=dest_primary_key, keep='first')

            print(f"\n🗓 Comparing 1-week window: {start_date} to {end_date}")
    
            # Column filtering based on mode
            mode = config["validation_config"]["column_comparison"]["mode"]
            if mode == "specific":
                selected_cols = config["validation_config"]["column_comparison"]["columns"]
                c_map = {k: v for k, v in col_mappings.items() if v in selected_cols}
            else:
                c_map = col_mappings

            print("Column mappings used for comparison:\n", c_map)

            # Perform comparison
            window_comparator = RowByRowComparator(src_window, dest_window, c_map, src_primary_key, dest_primary_key)
            window_comparator.compare() 

        except FileNotFoundError as e:
            print(f"File not found: {e.filename}")
        except pd.errors.ParserError as e:
            print("CSV parsing error:", e)
        except KeyError as e:
            print(f"Missing expected key: {e}")
        except ValueError as e:
            print(f"Value error: {e}")
        except Exception as e:
            print(f"Unexpected error ({type(e).__name__}): {e}")
            sys.exit(1)
