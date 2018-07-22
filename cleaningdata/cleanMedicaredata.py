

import pandas as pd

def citystate(x,y):
     return(x + ', ' + y)

def fips_standard(x):
    x = str(x).replace('.0','')
    if len(x) == 4:
        x = '0' + str(x)
    return(x)

##############################

# ACA primary care physician definition: from https://www.cms.gov/Regulations-and-Guidance/Guidance/Transmittals/downloads/R2161CP.pdf

# The ACA defines a primary care practitioner as: (1) a physician who has a primary specialty
# designation of family medicine, internal medicine, geriatric medicine, or pediatric medicine; or (2) a nurse
# practitioner, clinical nurse specialist, or physician assistant, and in all cases, for whom primary care services
# accounted for at least 60 percent of the allowed charges under Part B for the practitioner in a prior period as
# determined appropriate by the Secretary. 

# Load data
dataset = 'Medicare_Physician_and_Other_Supplier_NPI_Aggregate_CY2016.csv'
df = pd.read_csv(dataset, encoding = "ISO-8859-1", low_memory=False)#,header=4))

# Reference for matching city, state with county information
df2 = pd.read_csv(basedir + "allcitystatecounty.csv")
df2.set_index(keys = 'citystate',inplace=True)
df2.head()

# Create 'city, state' column to next get county information
df.dropna(axis=0, subset=['NPPES_PROVIDER_CITY'],inplace=True)
df['citystate'] = df.apply(lambda row: citystate(row['NPPES_PROVIDER_CITY'],row['NPPES_PROVIDER_STATE']), axis=1)
df['citystate'] = df['citystate'].str.lower()

# Join data with reference list that matches city, state with county information
df3 = df.join(df2[['county_fips','county_name','zips','lat','lng']],
              on='citystate',how='left',lsuffix='_1',rsuffix='_2')
print(df3.shape)
df3 = df3[['NPI','PROVIDER_TYPE','NPPES_CREDENTIALS','citystate','county_fips','county_name','zips','lat','lng']]
df3['NPPES_CREDENTIALS'] = df3['NPPES_CREDENTIALS'].str.replace('.','')#.rstrip(',')

# Now that we have county information, need to select providers that fall in the 'primary care' category

# First, keep all the entries of M.D.'s that fall in the primary care category
df_keep_MD = df3.loc[df3['PROVIDER_TYPE'].isin(['Internal Medicine','Geriatric Medicine','Pediatric Medicine',
                                   'Family Practice'])]

# Next, separately keep nurse practioners and PA's
df_keep_NP = df3.loc[df3['PROVIDER_TYPE'].isin(['Nurse Practitioner','Physician Assistant'])]

print("List of MD's: ", df_keep_MD.shape)
print("List of NP's: ", df_keep_NP.shape)

# Standardize FIPS column across all datasets
df_keep_MD['county_fips'] = df_keep_MD['county_fips'].apply(fips_standard)
df_keep_NP['county_fips'] = df_keep_NP['county_fips'].apply(fips_standard)

# Group entries by county FIPS, then get the counts for each county
df_MD_byCounty = df_keep_MD.groupby('county_fips').count()
df_NP_byCounty = df_keep_NP.groupby('county_fips').count()

df_MD_byCounty = df_MD_byCounty[['NPI','PROVIDER_TYPE']]
df_MD_byCounty.rename(columns = {'NPI': 'MD count','PROVIDER_TYPE': 'PROVIDER_TYPE1'},inplace=True)

df_NP_byCounty = df_NP_byCounty[['NPI','PROVIDER_TYPE']]
df_NP_byCounty.rename(columns = {'NPI':'NP count','PROVIDER_TYPE': 'PROVIDER_TYPE2'},inplace=True)

print(df_MD_byCounty.shape)
print(df_NP_byCounty.shape)

# Put MD counts and NP counts together in one dataframe, with total PC numbers
df_PC_byCounty_all = pd.concat([df_MD_byCounty, df_NP_byCounty], join='outer', axis=1, sort=True)
df_PC_byCounty_all['PC all'] = df_PC_byCounty_all['PROVIDER_TYPE1'] + df_PC_byCounty_all['PROVIDER_TYPE2']
df_PC_byCounty_all.drop(['PROVIDER_TYPE1','PROVIDER_TYPE2'],inplace=True,axis=1)

print(df_PC_byCounty_all.shape)
df_PC_byCounty_all.to_csv(basedir + 'county level datasets/' + 'medicareProvCount_MDandNP.csv')







