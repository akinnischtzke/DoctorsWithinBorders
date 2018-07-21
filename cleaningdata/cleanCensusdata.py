

import pandas as pd

def fips_standard(x):
    x = str(x).replace('.0','')  
    if len(x) == 4:
        x = '0' + str(x)
    return(x)


#####

basedir = 'https://raw.githubusercontent.com/akinnischtzke/DoctorsWithinBorders/master/cleaningdata/'

############### FOR POPULATION DATA ###############
dataset = 'PopulationEstimates.csv'

df = pd.read_csv(basedir + dataset,encoding = "ISO-8859-1",header=2)
# Keep only data from 2016
df2016 = df.loc[:, (df.columns.str.contains('2016'))]
# Recombine with region info (e.g. fips, county name, etc)
df2016_popdata = pd.concat([df[['FIPS','State','Area_Name','Rural-urban_Continuum Code_2013',]],
                            df2016[['POP_ESTIMATE_2016','N_POP_CHG_2016','R_birth_2016','R_death_2016']]],axis=1)
df2016_popdata.dropna(axis=0,subset=['FIPS'],inplace=True)
df2016_popdata['FIPS'] = df2016_popdata['FIPS'].astype(int)

print("Population data size: ",df2016_popdata.shape)


############### FOR POVERTY DATA ###############
dataset = 'PovertyEstimates.csv'

df = pd.read_csv(basedir + dataset,encoding = "ISO-8859-1",header=3)
# Keep only data from 2016
df2016 = df.loc[:, (df.columns.str.contains('POV'))]
# Recombine with region info (e.g. fips, county name, etc)
df2016_povdata = pd.concat([df[['FIPStxt']],df2016],axis=1)
print("Poverty data size: ",df2016_povdata.shape)

############### FOR EMPLOYMENT DATA ###############
dataset = 'Unemployment.csv'

df = pd.read_csv(basedir + dataset,encoding = "ISO-8859-1",header=7)
# Keep only data from 2016
df2016 = df.loc[:, (df.columns.str.contains('2016'))]
# Recombine with region info (e.g. fips, county name, etc)
df2016_empdata = pd.concat([df[['FIPStxt']],df2016],axis=1)
print("Employment data size: ",df2016_empdata.shape)
#df.columns

############### FOR EDCUATION DATA ###############
dataset = 'Education.csv'

df = pd.read_csv(basedir + dataset,encoding = "ISO-8859-1",header=4)
# Keep only data from 2016
df2016 = df.loc[:, (df.columns.str.contains('2016'))]
df2016 = df2016.loc[:, (df2016.columns.str.contains('Percent'))]

# Recombine with region info (e.g. fips, county name, etc)
df2016_edudata = pd.concat([df[['FIPS Code']],df2016],axis=1)
df2016_edudata.dropna(axis=0,subset=['FIPS Code'],inplace=True)
df2016_edudata['FIPS Code'] = df2016_edudata['FIPS Code'].astype(int)

print("Education data size: ",df2016_edudata.shape)

# Standardize FIPS column across all datasets, then set as index
df2016_popdata['county_fips'] = df2016_popdata.apply(lambda row: fips_standard(row['FIPS']), axis=1)
df2016_povdata['county_fips'] = df2016_povdata.apply(lambda row: fips_standard(row['FIPStxt']), axis=1)
df2016_empdata['county_fips'] = df2016_empdata.apply(lambda row: fips_standard(row['FIPStxt']), axis=1)
df2016_edudata['county_fips'] = df2016_edudata.apply(lambda row: fips_standard(row['FIPS Code']), axis=1)

# Use newly created 'county_fips' columns as the index for all df's 
df2016_popdata.set_index(keys=['county_fips'], inplace=True)
df2016_povdata.set_index(keys=['county_fips'], inplace=True)
df2016_empdata.set_index(keys=['county_fips'], inplace=True)
df2016_edudata.set_index(keys=['county_fips'], inplace=True)

df2016_alldata = pd.concat([df2016_popdata,
	df2016_povdata,df2016_empdata,
	df2016_edudata],axis=1,join='inner')

print("Combined size: ", df2016_alldata.shape)

df2016_alldata.to_csv("allCensus_allcounties.csv")




