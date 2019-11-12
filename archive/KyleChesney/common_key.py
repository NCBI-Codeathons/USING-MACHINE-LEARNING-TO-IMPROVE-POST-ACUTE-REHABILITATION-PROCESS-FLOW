# Search for candidates to act as a common key other than IHAR due to mismatches
import pandas as pd

# import all datasets
df_qual = pd.read_excel('data/uds_qualified_data.xlsx')
df_unq = pd.read_excel('data/uds_non-qualified_data.xlsx')
df_pat_hsp = pd.read_excel('data/pat_hsp.xlsx')
df_ins = pd.read_excel('data/insurance.xlsx')
df_rehab_pat = pd.read_excel('data/rehab_pat_dx_data.xlsx')
df_rehab_pat_matched = pd.read_excel('data/rehab_pat_matched_dx_data.xlsx')
df_rehab_pat_ = pd.read_excel('data/rehab_pat_matched_dx_data.xlsx')

# this should be a lambda...
for qual_key in df_qual.keys():
    if (qual_key in df_unq.keys()):
        if (qual_key in df_pat_hsp.keys()):
            if (qual_key in df_ins.keys()):
                print(qual_key)

