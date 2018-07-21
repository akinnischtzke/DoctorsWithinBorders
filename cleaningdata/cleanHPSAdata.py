

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from us import states


# the HPSA data:
database = 'BCD_HPSA_FCT_DET_PC.csv' # HPSA scores for primary care

# Full dataset
df_hpsa = pd.read_csv(database, low_memory=False)#,encoding = "ISO-8859-1")
print("Total dataset size: ", df_hpsa.shape)

# Drop all designations that are no longer active (NOTE: lose a lot of rows when doing this)
df_hpsa = df_hpsa.loc[df_hpsa['HPSA Status Description'] != 'Withdrawn']
print("Keeping only current designations: ", df_hpsa.shape)

# Save only the 'county' geographical areas, as opposed to census tract or facility (b/c most data for counties)
df_hpsa = df_hpsa.loc[df_hpsa['HPSA Component Type Description'] == 'Single County']
print("Save only single county data: ", df_hpsa.shape)

# We want to get the HPSA data by geographic region (as opposed to, e.g. population groups)
df_hpsa = df_hpsa.loc[df_hpsa['HPSA Type Description'] != 'Hpsa Population']
print("Remove data by population: ", df_hpsa.shape)

# Drop columns that are all NaN values
df_hpsa.dropna(how='all', axis=1, inplace=True)
print("Drop columns that are all Nan's: ", df_hpsa.shape)

# Drop several columns that we don't need, to make data easier to work with
df_hpsa.drop(labels = ['HPSA Source Name','HPSA Status Code',
                         'HPSA Type Code','HPSA State Abbreviation','HPSA Designation Last Update Date',
                         'HPSA Metropolitan Indicator Code','Discipline Class Number','Discipline Class Description',
                         'HPSA Component Status Code','HPSA Component Source Name','HPSA Component Status Description',
                         'HPSA Component Type Code','HPSA Component State Abbreviation',
                         'HPSA Component Designation Date','HPSA Component Designation Date String',
                         'HPSA Component Designation Last Update Date','Primary State Name','Primary State FIPS Code',
                         'Primary HHS Region Name','Data Warehouse Record Create Date','Data Warehouse Record Create Date Text',
                         'Break in Designation','HPSA Population Type Code','Common County Name','Common State County FIPS Code',
                         'Common State Abbreviation','Common State Name','Common State FIPS Code','Common Region Name',
                         'Provider Type'], axis=1, inplace=True)

print("Drop several columns we don't need: ", df_hpsa.shape)

# Duplicate entries for each HPSA component, which we're not interested in here
df_hpsa.drop_duplicates(subset=['County Equivalent Name'],inplace=True)
print("Remove duplicate county entries: ", df_hpsa.shape)

df_hpsa.to_csv('hpsa_data_cleaned.csv')



