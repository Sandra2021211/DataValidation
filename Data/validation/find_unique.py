import pandas as pd

df = pd.read_csv("/workspaces/DataValidation/Data/src_data/cleaned_insurance_claim_.csv")  # Replace with your actual path

df_copy = df.copy()

# Drop fully identical rows
df_copy = df_copy.drop_duplicates()

#  try claim_id -> only
unique_claim_ids = df_copy['claim_id'].nunique()

# try claim_id + patient_id 
df_copy['claim_patient'] = df_copy['claim_id'].astype(str) + '_' + df_copy['patient_id'].astype(str)
unique_claim_patient = df_copy['claim_patient'].nunique()

# try claim_id + patient_id + claim_segment
df_copy['claim_patient_segment'] = df_copy['claim_patient'] + '_' + df_copy['claim_segment'].astype(str)
unique_composite_keys = df_copy['claim_patient_segment'].nunique()

# Final counts
print("\n Unique Key Counts:")
print(f" Unique 'claim_id' count: {unique_claim_ids}")
print(f" Unique 'claim_id + patient_id' count: {unique_claim_patient}")
print(f" Unique 'claim_id + patient_id + claim_segment' count: {unique_composite_keys}")