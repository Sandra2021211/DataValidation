import pandas as pd
import json
import yaml


class DataValidator:
    def __init__(self, source_file, destination_file, config_file, mappings_file):
        self.source_file = source_file
        self.destination_file = destination_file
        self.config_file = config_file
        self.mappings_file = mappings_file
        self.source_df = None
        self.destination_df = None
        self.config = None
        self.mappings = None

    def load_data(self):
        # Load datasets
        self.source_df = pd.read_csv(self.source_file)
        self.destination_df = pd.read_csv(self.destination_file)

        # Load config and mappings
        with open(self.config_file, "r") as f:
            self.config = yaml.safe_load(f)
        with open(self.mappings_file, "r") as f:
            self.mappings = json.load(f)

        # Apply column mappings to source dataset
        column_mappings = self.mappings.get("column_mappings", {})
        self.source_df.rename(columns=column_mappings, inplace=True)

        # Add 'stream_time' column to datasets if needed
        if 'stream_time' not in self.source_df.columns or 'stream_time' not in self.destination_df.columns:
            print("Adding 'stream_time' column to datasets...")
            self.add_stream_time("2010-01-01", "2010-02-28")

    def add_stream_time(self, start_date, end_date):
        # Add a range of dates to the datasets
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        date_range = pd.date_range(start=start, end=end, periods=len(self.source_df))
        self.source_df['stream_time'] = date_range
        self.destination_df['stream_time'] = date_range.copy()

    def filter_date_range(self):
        # Filter datasets by date range specified in the config
        date_filter = self.config["validation_config"]["date_filter"]
        column = date_filter["column"]
        start = pd.to_datetime(date_filter["start_date"])
        end = pd.to_datetime(date_filter["end_date"])

        if column not in self.source_df.columns or column not in self.destination_df.columns:
            print(f"Error: Column '{column}' not found in the dataset.")
            return

        self.source_df = self.source_df[
            (self.source_df[column] >= start) & (self.source_df[column] <= end)
        ]
        self.destination_df = self.destination_df[
            (self.destination_df[column] >= start) & (self.destination_df[column] <= end)
        ]
        print(f"Filtered data from {start.date()} to {end.date()}.")

    def compare_datasets(self):
        # Extract primary key from mappings
        primary_key = self.mappings["validation_rules"]["primary_key"]

        if primary_key not in self.source_df.columns:
            print(f"Error: Primary key '{primary_key}' not found in the source dataset.")
            return
        if primary_key not in self.destination_df.columns:
            print(f"Error: Primary key '{primary_key}' not found in the destination dataset.")
            return

        # Compare rows by primary key
        mismatches = []
        for _, dest_row in self.destination_df.iterrows():
            key = dest_row[primary_key]
            src_row = self.source_df[self.source_df[primary_key] == key]

            if src_row.empty:
                mismatches.append(f"Primary key '{key}' not found in source dataset.")
                continue

            src_row = src_row.iloc[0]
            for col in self.destination_df.columns:
                if col in self.source_df.columns:
                    src_val = src_row[col]
                    dest_val = dest_row[col]
                    # Handle NaN comparison
                    if pd.isna(src_val) and pd.isna(dest_val):
                        continue  # Treat NaNs as equal
                    if src_val != dest_val:
                        mismatches.append(
                            f"Mismatch for key '{key}' in column '{col}': source='{src_val}', destination='{dest_val}'"
                        )

        if mismatches:
            print(f"Total mismatches found: {len(mismatches)}")
            with open("mismatches.txt", "w") as f:
                f.writelines(mismatch + "\n" for mismatch in mismatches)
            print("Mismatch details written to 'mismatches.txt'.")
        else:
            print("No mismatches found.")

    def validate(self):
        self.load_data()
        self.filter_date_range()
        self.compare_datasets()


if __name__ == "__main__":
    # File paths
    source_file = "/workspaces/DataValidation/data/src_data/insurance_Claim_.csv"
    destination_file = "/workspaces/DataValidation/data/src_data/cleaned_insurance_claim_.csv"
    config_file = "/workspaces/DataValidation/data/src_data/config.yaml"
    mappings_file = "/workspaces/DataValidation/data/src_data/insurance_mapping.json"

    # Initialize validator and run validation
    validator = DataValidator(source_file, destination_file, config_file, mappings_file)
    validator.validate()
