import pandas as pd 
import time

class RowByRowComparator:
    def __init__(self,source_df,dest_df,col_mappings,src_primary_key,dest_primary_key):
        self.source_df=source_df.copy()
        self.dest_df=dest_df.copy()
        self.col_mappings=col_mappings
        self.src_primary_key=src_primary_key
        self.dest_primary_key=dest_primary_key

        #print("Source columns:", self.source_df.columns.tolist())
        #print("Destination columns:", self.dest_df.columns.tolist())


        #Set index for fast row access using primary key
        self.source_df.set_index(src_primary_key,inplace=True)
        self.dest_df.set_index(dest_primary_key,inplace=True)

    def compare(self):
        print("\nRow by Row comparison:")
        start_time=time.time() #Start time

        mismatch=[]

        #Iterate through each row in source df
        for k in self.source_df.index:
            if k not in self.dest_df.index:
                mismatch.append((k,"row","missing in destination"))
                continue

            src_row=self.source_df.loc[k]
            dest_row=self.dest_df.loc[k]

            for src_col,dest_col in self.col_mappings.items():
                if src_col in src_row and dest_col in dest_row:
                    src_val=src_row[src_col]
                    dest_val=dest_row[dest_col]
                    
                    #if values are NULL, then continue

                    if pd.isnull(src_val) and pd.isnull(dest_val):
                        continue

                    #Compare values and appends mismatch to the list

                    elif src_val!=dest_val:
                        mismatch.append((k,src_col,dest_col,src_val,dest_val))

        if mismatch:
            print("Mismatches found:")
            for mis in mismatch:
                if len(mismatch)==3:
                    print(f"Row {mis[0]}: {mis[2]}")
                else:
                    print(f"Row {mis[0]} | Source: {mis[1]}-{mis[3]} , Destination: {mis[2]}-{mis[4]}")
        else:
            print("All rows match!!!")

        end_time=time.time() #End time
        time_diff=end_time-start_time
        print(f"Time taken for row-by-row comparison: {time_diff:.2f} seconds")
