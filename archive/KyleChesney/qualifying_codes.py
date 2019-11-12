# This file contains (messy) code used to find diagnosis codes whcih appeared assigned to
# both qualified and unqualified patients, identifying records with errors and common sources of error.
# This file was also used to mark patients who suffered a hemispheric stroke to use that as a feature for the model.
# Namrata was heavily involved in the writing of this script.
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

df_qual = pd.read_csv('data/FinalData.csv')
df_unq = pd.read_excel('data/uds_non-qualified_data.xlsx')
df_ins = pd.read_excel('data/uds_insurance.xlsx')
df_pat_hsp = pd.read_excel('data/pat_hsp.xlsx')


df_UDS_impairment = pd.read_excel('data/UDSdata.xlsx', sheet_name='Q_Admission_Imp')
df_UDS_etiologic = pd.read_excel('data/UDSdata.xlsx', sheet_name='Q_Etilogic_Diag')
df_UDS_comorbid = pd.read_excel('data/UDSdata.xlsx', sheet_name='Q_Comorbid')

df_qual_hsp = df_pat_hsp.merge(df_qual, on='IHAR', how = 'left')

df_qual_hsp['etiologic_based'] = df_qual_hsp['IRF'].apply(lambda x: x in ['Qualifying Comorbid condition', 'Qualifying Etiologic condition'])


import scipy.stats as scs

def categories(series):
    return range(int(series.min()), int(series.max()) + 1)

def chi_square_of_df_cols(df, col1, col2):
    df_col1, df_col2 = df[col1], df[col2]
    cats1, cats2 = categories(df_col1), categories(df_col2)
    def aux(is_cat1):
        return [sum(is_cat1 & (df_col2 == cat2))
                for cat2 in cats2]
    result = [aux(df_col1 == cat1)
              for cat1 in cats1]
    return scs.chi2_contingency(result)

chi_square_of_df_cols(df_qual, 'etiologic_based', 'ONSET_DAYS')
#unq_ICD10 = df_unq['ADM_IMPAIR_CODE'].unique()

qual_ICD10 == unq_ICD10 # not useful
any(qual_ICD10) in unq_ICD10 # also not useful :(

def find_questionable_ICD10(df_qualified, test_code):
    # What are all qualifying ICD10 codes listed?
    qual_codes = df_qualified[test_code].unique()
    nonqualifiying_codes = df_unq[test_code].unique()
    questionable = []
    # separate out which ICD10 codes are assigned to both qualified and unqualified patients
    for i in qual_codes:
        if (i in nonqualifiying_codes):
            questionable.append(i)
    df_qual_w_questionable_codes = df_qualified.loc[df_qual[test_code].isin(questionable)]
    return df_qual_w_questionable_codes

overall_common_ICD = find_questionable_ICD10(df_qual, 'ETIOLOGIC_DX') # total
q_ICD_impairment = find_questionable_ICD10(df_UDS_impairment, 'ETIOLOGIC_DX') # impairment
q_ICD_etiologic= find_questionable_ICD10(df_UDS_etiologic, 'ETIOLOGIC_DX') # etiologic

# special case for comorbid
qual_comorbid_codes = df_UDS_comorbid['COMORBID_ICD_1'].unique()
nonqualifiying_ICD10_codes = df_unq['ETIOLOGIC_DX'].unique()
questionable_comorbid = []

for i in qual_comorbid_codes:
    if (i in nonqualifiying_ICD10_codes):
        questionable_comorbid.append(i)

df_qual_w_questionable_comorbid_codes = df_qual.loc[df_qual[test_code].isin(questionable)]
q_ICD_comorbid = find_questionable_ICD10(df_UDS_comorbid, 'COMORBID_ICD_1') # etiologic

overall_common_impair = find_questionable_ICD10(df_qual, 'ADM_IMPAIR_CODE')
q_ADM_impairment = find_questionable_ICD10(df_UDS_impairment, 'ADM_IMPAIR_CODE') # impairment
q_ADM_etiologic= find_questionable_ICD10(df_UDS_etiologic, 'ADM_IMPAIR_CODE') # etiologic
q_ADM_comorbid= find_questionable_ICD10(df_UDS_comorbid, 'ADM_IMPAIR_CODE') # etiologic


for i in df_unq['ETIOLOGIC_DX']:
    print(i in questionable)

len(unq_ICD10)
len(qual_ICD10)

df_qual = df_qual.merge(df_ins, on='IHAR', how='left')

# separate people into stroke or non-stroke
df_qual['HEMISPHERIC_STROKE'] = df_qual['ADM_IMPAIR_CODE'].apply(lambda x: int(x in [1.1, 1.2]))

df_qual[df_qual['HEMISPHERIC_STROKE'] == 0]
df_qual[df_qual['HEMISPHERIC_STROKE'] == 1]


# preliminary graphic analysis
sns.barplot(x = 'y_actual', y = 'ONSET_DAYS', hue = 'HEMISPHERIC_STROKE', data = df_qual)
plt.show()

# What percentage of people have had a stroke?
df_qual \
.groupby('HEMISPHERIC_STROKE') \
.count()

stroke_1 = df_qual[df_qual['HEMISPHERIC_STROKE'] == 1]

# Stroke patients do not differ much except for in the "high" classification
# where patients who have suffered a stroke actually spend less time

chi2, p, dof, expected = stats.chi2_contingency(pd.crosstab(df_qual['y_actual'], df_qual['HEMISPHERIC_STROKE']))
stats.chi2_contingency(pd.crosstab(df_qual['y_actual'], df_qual['HEMISPHERIC_STROKE']))

crit = stats.chi2.ppf(q = 0.95, df = 1)

pd.crosstab(df_qual['HEMISPHERIC_STROKE'], df_qual['y_actual'])

((df_qual[df_qual['HEMISPHERIC_STROKE'] == 1] - df_qual)**2 / df_qual).sum()

df_qual[df_qual['HEMISPHERIC_STROKE'] == 1]['PRIM_PAYOR_SRC'].unique()

