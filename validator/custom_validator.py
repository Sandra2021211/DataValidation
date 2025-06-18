import pandas as pd 
from file_read import FileReader
from stream import StreamingData
from row_by_row_comparison import RowByRowComparator

class CustomDatasetValidator:
    def __init__(self, src_path, dest_path, map_path, yaml_path):
        self.src_path = src_path
        self.dest_path = dest_path
        self.map_path = map_path
        self.yaml_path = yaml_path

    def run(self):

        # Read files
        test_src_df = FileReader.read_csv(self.src_path, parse_dates=['stream_time'])
        test_dest_df = FileReader.read_csv(self.dest_path, parse_dates=['stream_time'])
        mapping = FileReader.read_json(self.map_path)
        config = FileReader.read_yaml(self.yaml_path)

        col_mappings = mapping["column_mappings"]
        src_primary_key = "CLM_ID"
        dest_primary_key = "claim_id"

        #print("Source datatypes:",test_src_df.dtypes)
        #print("Destination datatypes:",test_dest_df.dtypes)

        #print("Sample Destination Row:", test_dest_df.iloc[0])
        #print("Sample Source Row:", test_src_df.iloc[0])

        # Get corrupted date window

        stream = StreamingData(test_src_df, test_dest_df)
        start_date = config["validation_config"]["date_filter"]["start_date"]
        end_date = config["validation_config"]["date_filter"]["end_date"]

        src_window, dest_window = stream.corrupted_dateframe(start_date, end_date)

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
