import pandas as pd
from datetime import datetime, timedelta

# Step 1: Read your original CSV and force all columns as strings
df = pd.read_csv('src_data/d.csv', dtype=str)

# Step 2: Add the `stream_time` column with 62 sequential dates from 2025-04-01
start_date = datetime(2025, 4, 1)
stream_dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(len(df))]
df['stream_time'] = stream_dates

# Step 3: Save the new dataset (preserving all data as string)
df.to_csv('src_data/dest_with_stream_time.csv', index=False)
