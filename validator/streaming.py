import pandas as pd
import numpy as np

class StreamingData:
    def __init__(self,src_df,dest_df):
        self.src_df=src_df
        self.dest_df=dest_df

    #To add dates for a time period of two months to the data frame

    def add_date(self,start_date, end_date):
        start=pd.to_datetime(start_date)
        end=pd.to_datetime(end_date)

        date_range=pd.date_range(start=start, end=end, periods=len(self.src_df))
        self.src_df['stream_time']=date_range
        self.dest_df['stream_time']=date_range.copy()

    #To add 1 week window for corrupted data

    def corrupted_dateframe(self,start,end):
        c_start=pd.to_datetime(start)
        c_end=pd.to_datetime(end)

        src_window=self.src_df[(self.src_df['stream_time']>=c_start) & (self.src_df['stream_time']<=c_end)]
        dest_window=self.dest_df[(self.dest_df['stream_time']>=c_start) & (self.dest_df['stream_time']<=c_end)]

        return src_window,dest_window