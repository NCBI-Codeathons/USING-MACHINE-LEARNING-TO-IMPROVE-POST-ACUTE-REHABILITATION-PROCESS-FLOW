import pandas as pd

# scrape Excel files dataframes
df_qual = pd.read_excel('data/uds_qualified_data.xlsx')
df_unq = pd.read_excel('data/uds_non-qualified_data.xlsx')
df_pat_hsp = pd.read_excel('data/pat_hsp.xlsx')

###
### Analysis of qualified patients
###

# Note that joining on PATIENT_NUM incurs some data loss
# due to df_qual containing missing PATIENT_NUM
# IHAR does not result in NaN entries, but there are only _21_
df_qual_hsp = df_pat_hsp.merge(df_qual, on='PATIENT_NUM')

# which % of Q admitted patients are coming from Zale, Clements?
qual_ref_count = df_qual_hsp \
.groupby('POS_NAME') \
.count()

# What % of Qualifying patients came from where?
# Keyed on SRC to limit to 1 column
print('What % of Qualifying patients came from where?')
((qual_ref_count / qual_ref_count.sum()) * 100).sort_values('SRC', ascending = 0)['SRC']

### 
### Analysis of NQ patients
### 

#TODO: check up on IHAR as common key
df_unq_hsp = df_pat_hsp.merge(df_unq, on='PATIENT_NUM')

# What % of NQ patients came from where?
unq_ref_count = df_unq_hsp \
.groupby('POS_NAME') \
.count()
((unq_ref_count / unq_ref_count.sum()) * 100).sort_values('SRC', ascending = 0)['SRC']

# which services are sending NQ diagnosis patients?
df_unq_hsp['HOSP_SERVICE'] \
.unique()

# what services are sending what number of unqualified patients?
unq_serv_count = df_unq_hsp \
.groupby(['HOSP_SERVICE','POS_NAME']) \
.count()

unq_serv_count.sort_values('SRC', ascending=0)['SRC']

# What percentage of NQ patients are sent from each service?
((unq_serv_count / unq_serv_count.sum()) * 100).sort_values('SRC', ascending = 0)['SRC']
