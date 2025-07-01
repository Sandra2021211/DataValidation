import pandas as pd
from datetime import datetime, timedelta
import numpy as np

df = pd.read_csv('/workspaces/DataValidation/data/src_data/cleaned_insurance_claim_.csv', dtype=str)

start_date = datetime(2025, 4, 1)
end_date = datetime(2025, 5, 31)

num_rows = len(df)

date_range = pd.date_range(start=start_date, end=end_date, freq='D')

repeated_dates = np.tile(date_range, int(np.ceil(num_rows / len(date_range))))[:num_rows]
df['stream_time'] = pd.to_datetime(repeated_dates).strftime('%Y-%m-%d')
df.to_csv('/workspaces/DataValidation/data/src_data/cleaned_insurance_claim_.csv', index=False)