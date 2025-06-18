import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Step 1: Read your original CSV and keep all columns as strings
df = pd.read_csv('/workspaces/DataValidation/data/src_data/expanded_destination.csv', dtype=str)

# Step 2: Define your start and end date
start_date = datetime(2025, 4, 1)
end_date = datetime(2025, 5, 31)

# Step 3: Generate 6001 dates uniformly distributed between the range
num_rows = len(df)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Repeat dates to match 6001 values
repeated_dates = np.tile(date_range, int(np.ceil(num_rows / len(date_range))))[:num_rows]
df['stream_time'] = pd.to_datetime(repeated_dates).strftime('%Y-%m-%d')

# Step 4: Save the new DataFrame without changing datatypes
df.to_csv('/workspaces/DataValidation/data/src_data/expanded_destination.csv', index=False)