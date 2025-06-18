import pandas as pd
import yaml
import json

class FileReader:
    @staticmethod
    def read_csv(file_path, **kwargs):
        return pd.read_csv(file_path, **kwargs)

    @staticmethod
    def read_json(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def read_yaml(file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)


class StreamDataProcessor:
    def __init__(self, source_df, destination_df):
        self.source_df = source_df
        self.destination_df = destination_df

    def filter_date_range(self, start_date, end_date):
        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date)

        print("Source stream_time range:", self.source_df['stream_time'].min(), "to", self.source_df['stream_time'].max())
        print("Destination stream_time range:", self.destination_df['stream_time'].min(), "to", self.destination_df['stream_time'].max())

        filtered_source = self.source_df[
            (self.source_df['stream_time'] >= start_datetime) & (self.source_df['stream_time'] <= end_datetime)
        ]
        filtered_destination = self.destination_df[
            (self.destination_df['stream_time'] >= start_datetime) & (self.destination_df['stream_time'] <= end_datetime)
        ]

        print("Filtered source size:", len(filtered_source))
        print("Filtered destination size:", len(filtered_destination))

        return filtered_source, filtered_destination


class RowComparator:
    def __init__(self, source_data, destination_data, column_mappings, source_key, destination_key):
        self.source_data = source_data.copy()
        self.destination_data = destination_data.copy()
        self.column_mappings = column_mappings
        self.source_key = source_key
        self.destination_key = destination_key

        self.source_data.set_index(source_key, inplace=True)
        self.destination_data.set_index(destination_key, inplace=True)

    def compare_rows(self):
        print("\nPerforming row-by-row comparison:")
        mismatches = []

        for key in self.source_data.index:
            if key not in self.destination_data.index:
                mismatches.append((key, "row", "missing in destination"))
                continue

            source_row = self.source_data.loc[key]
            destination_row = self.destination_data.loc[key]

            for source_column, destination_column in self.column_mappings.items():
                if source_column in source_row and destination_column in destination_row:
                    source_value = source_row[source_column]
                    destination_value = destination_row[destination_column]

                    if pd.isnull(source_value) and pd.isnull(destination_value):
                        continue
                    elif str(source_value) != str(destination_value):
                        mismatches.append((key, source_column, destination_column, source_value, destination_value))

        if mismatches:
            print("Mismatches found:")
            for mismatch in mismatches:
                if len(mismatch) == 3:
                    print(f"Row {mismatch[0]}: {mismatch[2]}")
                else:
                    print(f"Row {mismatch[0]} | Source: {mismatch[1]} → {mismatch[3]} , Destination: {mismatch[2]} → {mismatch[4]}")
        else:
            print("All rows match!")


def main():
    source_file_path = "/workspaces/DataValidation/data/src_data/expanded_source.csv"
    destination_file_path = "/workspaces/DataValidation/data/src_data/expanded_destination.csv"
    mapping_file_path = "/workspaces/DataValidation/data/src_data/insurance_mapping.json"
    config_file_path = "/workspaces/DataValidation/data/src_data/details.yaml"

    source_data = FileReader.read_csv(source_file_path, parse_dates=['stream_time'])
    destination_data = FileReader.read_csv(destination_file_path, parse_dates=['stream_time'])
    column_mapping = FileReader.read_json(mapping_file_path)
    configuration = FileReader.read_yaml(config_file_path)

    column_mappings = column_mapping["column_mappings"]
    source_primary_key = "CLM_ID"
    destination_primary_key = "claim_id"

    data_processor = StreamDataProcessor(source_data, destination_data)
    start_date = configuration["validation_config"]["date_filter"]["start_date"]
    end_date = configuration["validation_config"]["date_filter"]["end_date"]

    filtered_source, filtered_destination = data_processor.filter_date_range(start_date, end_date)

    filtered_source = filtered_source.drop_duplicates(subset=source_primary_key, keep='first')
    filtered_destination = filtered_destination.drop_duplicates(subset=destination_primary_key, keep='first')

    print(f"\nComparing data within the range: {start_date} to {end_date}")

    comparison_mode = configuration["validation_config"]["column_comparison"]["mode"]
    if comparison_mode == "specific":
        selected_columns = configuration["validation_config"]["column_comparison"]["columns"]
        filtered_column_mappings = {k: v for k, v in column_mappings.items() if v in selected_columns}
    else:
        filtered_column_mappings = column_mappings

    print("Column mappings used for comparison:\n", filtered_column_mappings)

    comparator = RowComparator(filtered_source, filtered_destination, filtered_column_mappings, source_primary_key, destination_primary_key)
    comparator.compare_rows()


if __name__ == "__main__":
    main()
