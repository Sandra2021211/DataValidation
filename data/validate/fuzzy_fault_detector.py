import os
import pandas as pd
import numpy as np
from difflib import SequenceMatcher


class RandomizedFuzzyValidator:
    def __init__(self, source_file, destination_file, similarity_threshold=75):
        self.source_file = source_file
        self.destination_file = destination_file
        self.similarity_threshold = similarity_threshold  # Threshold as a percentage
        self.source_df = None
        self.destination_df = None
        self.random_subset = None
        self.mismatched_data = []
        self.manual_column_mapping = {
            "Patient_ID": "Patient_Reference",
            "Admission_Date": "Admit_Date",
            "Discharge_Date": "Release_Date",
        }  # Add manual mappings here.

    def load_data(self):
        """Load datasets into Pandas DataFrames."""
        try:
            self.source_df = pd.read_csv(self.source_file)
            self.destination_df = pd.read_csv(self.destination_file)
        except Exception as e:
            raise Exception(f"Error loading data: {e}")

    def match_columns(self):
        """Dynamically map columns based on similarity with manual fallback."""
        source_cols = self.source_df.columns.tolist()
        destination_cols = self.destination_df.columns.tolist()

        print(f"Source Columns: {source_cols}")
        print(f"Destination Columns: {destination_cols}")

        column_mapping = {}
        for src_col in source_cols:
            if src_col in self.manual_column_mapping:
                column_mapping[src_col] = self.manual_column_mapping[src_col]
                continue

            best_match = None
            best_score = 0
            for dest_col in destination_cols:
                score = SequenceMatcher(None, src_col, dest_col).ratio()
                percentage_score = round(score * 100, 2)  # Convert to percentage
                print(f"Matching '{src_col}' with '{dest_col}' - Similarity: {percentage_score}%")
                if percentage_score > best_score and percentage_score >= self.similarity_threshold:
                    best_match = dest_col
                    best_score = percentage_score

            if best_match:
                column_mapping[src_col] = best_match

        print(f"Final Column Mapping: {column_mapping}")
        if not column_mapping:
            raise ValueError("No columns matched between source and destination datasets.")
        return column_mapping

    def random_sample_validation(self):
        """Select 25% of the data for validation."""
        source_sample_size = max(1, len(self.source_df) // 4)
        destination_sample_size = max(1, len(self.destination_df) // 4)

        self.random_subset = {
            "source": self.source_df.sample(n=source_sample_size, random_state=42),
            "destination": self.destination_df.sample(n=destination_sample_size, random_state=42),
        }

    def calculate_similarity(self, value1, value2):
        """Calculate similarity between two values."""
        if pd.isnull(value1) or pd.isnull(value2):  # Handle NaN values
            return 0
        if isinstance(value1, str) and isinstance(value2, str):
            return SequenceMatcher(None, value1, value2).ratio()
        try:
            # Handle numerical similarity (e.g., rounding issues)
            return 1 if np.isclose(float(value1), float(value2), atol=0.01) else 0
        except ValueError:
            return 0  # If non-numeric and not strings

    def validate_subset(self, column_mapping):
        """Validate a random subset of the data."""
        source_sample = self.random_subset["source"]
        destination_sample = self.random_subset["destination"]

        for _, source_row in source_sample.iterrows():
            is_matched = False
            for _, destination_row in destination_sample.iterrows():
                similarity_scores = []
                for src_col, dest_col in column_mapping.items():
                    src_value = source_row.get(src_col)
                    dest_value = destination_row.get(dest_col)
                    similarity = self.calculate_similarity(src_value, dest_value) * 100  # Convert to percentage
                    similarity_scores.append(similarity)

                if similarity_scores:
                    average_similarity = sum(similarity_scores) / len(similarity_scores)
                else:
                    average_similarity = 0

                print(f"Row Similarity: {average_similarity:.2f}%")
                if average_similarity >= self.similarity_threshold:
                    is_matched = True
                    break

            if not is_matched:
                self.mismatched_data.append(source_row)

    def export_results(self, output_file):
        """Export mismatched data to a CSV file."""
        output_directory = os.path.dirname(output_file)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        if self.mismatched_data:
            mismatched_df = pd.DataFrame(self.mismatched_data)
            mismatched_df.to_csv(output_file, index=False)
            print(f"Mismatched data exported to {output_file}")
        else:
            print("No mismatched data to export.")

    def run_validation(self, output_file):
        """Run the complete validation process."""
        self.load_data()
        print("Data loaded successfully.")

        # Map columns dynamically
        column_mapping = self.match_columns()

        # Select random subset
        self.random_sample_validation()
        print("Random subset selected for validation.")

        # Validate random subset
        self.validate_subset(column_mapping)
        print(f"Validation completed. Found {len(self.mismatched_data)} mismatched rows.")

        # Export results
        self.export_results(output_file)


# Usage
source_file = '/workspaces/DataValidation/data/src_data/hos_src.csv'
destination_file = '/workspaces/DataValidation/data/src_data/hos_dst.csv'
output_file = './output/mismatched_data.csv'

validator = RandomizedFuzzyValidator(source_file, destination_file, similarity_threshold=75)
try:
    validator.run_validation(output_file)
except Exception as e:
    print(f"Error: {e}")
