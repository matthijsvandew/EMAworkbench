import pandas as pd
import numpy as np

df_roads = pd.read_csv('_roads3.csv')
#print(df.head)
#print(df.columns)

df_roads = df_roads.drop(columns='gap')
#print(df_roads.columns)

df_bmms = pd.read_excel('BMMS_overview.xlsx')
#print(df_bmms.head)

df_bmms = df_bmms.drop(df_bmms[df_bmms['road'] != 'N1'].index)
df_roads = df_roads.drop(df_roads[df_roads['road'] != 'N1'].index)

#print(df_bmms)
#print(df_roads)

df_roads = df_roads.rename(columns={'lrp':'LRPName'})

df_bmms = df_bmms.drop_duplicates(subset=['LRPName'])

df_roads = df_roads.rename(columns={'lrp':'LRPName'})

merge_inner = df_bmms.merge(df_roads, how = 'right',on=['LRPName','road'])

#print(merge_inner['lon_y'].isna().sum()) # Geen missing values!
#print(merge_inner['lon_x'].isna().sum()) # 924 missing values!
#print(merge_inner['lat_y'].isna().sum()) # Geen missing values!
#print(merge_inner['lat_x'].isna().sum()) # 924 missing values
#print(merge_inner['length'].isna().sum()) # 924 missing values. Voor missing values length oplossing: als length == NaN: vervang NaN door verschil chainage i en i+1. Dat kan omdat dit roads zijn en geen bridges. Voor bridges is namelijk geen NaN value bij length.
#print(merge_inner['chainage_x'].isna().sum()) # 924 missing values
#print(merge_inner['chainage_y'].isna().sum()) # Geen missing values!
#print(merge_inner['type_x'].isna().sum()) # 924 missing values
#print(merge_inner['name_x'].isna().sum()) # 924 missing values
#print(merge_inner['type_y'].isna().sum()) # Geen missing values!
#print(merge_inner['name_y'].isna().sum()) # Geen missing values

#print(merge_inner.length[2]) # kan allebei
#print(merge_inner.loc[2,'length']) # kan allebei

for i in range(len(merge_inner['length'])-1):
    if np.isnan(merge_inner.loc[i,'length']) == True:
        merge_inner.loc[i,'length'] = (merge_inner.chainage_y[i+1] - merge_inner.chainage_y[i])
        #print(merge_inner.loc[i,'length'])

merge_inner = merge_inner[['road','LRPName','length','chainage_y','lon_y','lat_y','type_y','name_y','condition']]
print(merge_inner)

merge_inner.to_csv(r"C:\Github\epa1352advancedsimulation\assignment_2\EPA1352-G13-A2\data\demo_try_self.csv",index=False)