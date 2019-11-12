# This code was used (repeatedly) to accomplish my initial assignment,
# identifying institutions and services responsible for which portions of
# qualified and unqualified patients
import pandas as pd
import seaborn as sns

# scrape Excel files dataframes
#df_qual = pd.read_excel('data/uds_qualified_data.xlsx')
df_qual = pd.read_csv('data/FinalData.csv')
df_unq = pd.read_excel('data/uds_non-qualified_data.xlsx')
df_pat_hsp = pd.read_excel('data/pat_hsp.xlsx')

df_qual['QUALIFIED'] = 1
df_unq['QUALIFIED'] = 0

###
### Analysis of qualified patients
###

# Note that joining on PATIENT_NUM incurs some data loss
# due to df_qual containing missing PATIENT_NUM
# IHAR does not result in NaN entries, but there are only _21_
df_qual_hsp = df_pat_hsp.merge(df_qual, on='PATIENT_NUM')

df_unq_hsp = df_pat_hsp.merge(df_unq, on='PATIENT_NUM')

# Combine institutions
clements = ['CUH RADIOLOGY', 'CUH NEUROLOGY', 'CUH PATHOLOGY', 'CUH Emergency Medicine', 'CUH INTERNAL MEDICINE']
zale = ['UHZL RADIOLOGY', 'ZLUH ORS']

df_qual_hsp['POS_NAME'].replace(clements, 'Clements University Hospital', inplace = True)
df_qual_hsp['POS_NAME'].replace(zale , 'ZALE LIPSHY UNIVERSITY HOSPITAL', inplace = True)

df_unq_hsp['POS_NAME'].replace(clements, 'Clements University Hospital', inplace = True)
df_unq_hsp['POS_NAME'].replace(zale , 'ZALE LIPSHY UNIVERSITY HOSPITAL', inplace = True)

# combine datasets
df = df_qual_hsp.append(df_unq_hsp)

# which % of Q admitted patients are coming from Zale, Clements?
qual_ref_count = df_qual_hsp \
.groupby('POS_NAME') \
.count()

# What % of Qualifying patients came from where?
print('What % of Qualifying patients came from where?')
qualifying_counts = ((qual_ref_count / qual_ref_count.sum()) * 100).sort_values('SRC', ascending = 0)['SRC']


qual_serv_count = df_qual_hsp \
.groupby(['HOSP_SERVICE','POS_NAME']) \
.count()

qual_serv_tbl = qual_serv_count.sort_values('SRC', ascending=0)['SRC'] \
.reset_index()

sns.barplot(x = 'HOSP_SERVICE', y = 'SRC', hue = 'POS_NAME', data = qual_serv_tbl.head(5))
plt.show()

sns.barplot
#
### 
### Analysis of NQ patients
### 

#TODO: check up on IHAR as common key
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

def analyze_referring_inst(df_hsp_combo):
    # What % of patients came from where?
    ref_count = df_hsp_combo \
    .groupby('POS_NAME') \
    .count()
    print("Where are patients coming from?")
    print(((ref_count / ref_count.sum()) * 100).sort_values('SRC', ascending = 0)['SRC'])
    # which services are sending these patients?
    df_hsp_combo['HOSP_SERVICE'] \
    .unique()
    # what services, from  are sending what number of patients?
    df_serv_count = df_hsp_combo \
    .groupby(['HOSP_SERVICE','POS_NAME']) \
    .count()
    df_serv_count.sort_values('SRC', ascending=0)['SRC']
    # What percentage of NQ patients are sent from each service?
    ((df_serv_count / df_serv_count.sum()) * 100).sort_values('SRC', ascending = 0)['SRC']

