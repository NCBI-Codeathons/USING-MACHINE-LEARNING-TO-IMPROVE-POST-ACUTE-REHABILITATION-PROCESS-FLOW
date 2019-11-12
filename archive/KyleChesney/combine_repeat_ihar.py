# We noticed that what should be a unique visit identifier, IHAR, was repeating
# the cause was that patients transferred out or taking leave were listed as being discharged and readmitted
# but they were not assigned a new visit identifier.

# Our solution to clean this was to identify duplicate IHARs, and condense them into one visit
# by using only the earliest admission and latest discharge, all other columns for these entries were identical.
# Akshay solved this problem via other methods directly in Pandas,
# this code is left here for essentially sentimental reasons
from datetime import datetime as dt

df_qual = pd.read_csv('data/FinalData.csv')
repeat_ihars = df_qual[df_qual['IHAR'].duplicated()]['IHAR'].unique()

df_qual['date_delta'] = df_qual['HOSP_DISCH_TIME'] - df_qual['HOSP_ADMSN_TIME']

# IHAR: {min: xx, max: yy}
ihar_intermediary = {}
time_format = '%d-%b-%Y %H:%M:%S'

for index, row in df_qual.iterrows():
    ihar = (row['IHAR'])
    if (ihar in repeat_ihars):
        this_adm = row['HOSP_ADMSN_TIME']
        print(this_adm)
        this_dsch = row['HOSP_DISCH_TIME']
        if (ihar not in ihar_intermediary):
            if (np.isnan(this_adm) | np.isnan(this_dsch)):
                continue
            else:
                ihar_intermediary[ihar] = {'min_adm': this_adm, 'max_disch': this_dsch}
        else:
            if (np.isnan(this_adm) | np.isnan(this_dsch)):
                continue
            print(this_adm_time)
            this_adm_dt = dt.strptime(this_adm, time_format)
            this_dsch_dt = dt.strptime(this_dsch, time_format)

