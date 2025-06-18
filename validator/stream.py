import pandas as pd

class StreamingData:
    def __init__(self, src_df, dest_df):
        self.src_df = src_df
        self.dest_df = dest_df

    def corrupted_dateframe(self, start, end):
        c_start = pd.to_datetime(start)
        c_end = pd.to_datetime(end)

        #self.src_df['stream_time'] = pd.to_datetime(self.src_df['stream_time'])
        #self.dest_df['stream_time'] = pd.to_datetime(self.dest_df['stream_time'])

        print("✅ Source stream_time range:", self.src_df['stream_time'].min(), "to", self.src_df['stream_time'].max())
        print("✅ Dest stream_time range:", self.dest_df['stream_time'].min(), "to", self.dest_df['stream_time'].max())


        src_window = self.src_df[(self.src_df['stream_time'] >= c_start) & (self.src_df['stream_time'] <= c_end)]
        dest_window = self.dest_df[(self.dest_df['stream_time'] >= c_start) & (self.dest_df['stream_time'] <= c_end)]

        print("🔸 Source window size:", len(src_window))
        print("🔸 Destination window size:", len(dest_window))


        return src_window, dest_window