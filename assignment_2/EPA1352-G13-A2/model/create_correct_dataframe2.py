import pandas as pd
import numpy as np

df_roads = pd.read_csv('_roads3.csv')
df_roads = df_roads.drop(columns='gap')
df_bmms = pd.read_excel('BMMS_overview.xlsx')

df_bmms = df_bmms.drop(df_bmms[df_bmms['road'] != 'N1'].index)
df_roads = df_roads.drop(df_roads[df_roads['road'] != 'N1'].index)


df_roads = df_roads.rename(columns={'lrp':'LRPName'})
df_bmms = df_bmms.drop_duplicates(subset=['LRPName'])
df_roads = df_roads.rename(columns={'lrp':'LRPName'})

for i in range(len(df_roads['chainage'])): #chainage omzetten naar meters, want dat is lengte ook.
    df_roads.loc[i,'chainage'] = (df_roads.loc[i,'chainage'] * 1000)

merge_inner = df_bmms.merge(df_roads, how = 'right',on=['LRPName','road'])

#Check which one must be selected for the final dataset
#print(merge_inner['lon_y'].isna().sum()) # No missing values!
#print(merge_inner['lon_x'].isna().sum()) # 924 missing values!
#print(merge_inner['lat_y'].isna().sum()) # No missing values!
#print(merge_inner['lat_x'].isna().sum()) # 924 missing values
#print(merge_inner['length'].isna().sum()) # 924 missing values. --> Must be fixed. solution: if length == NaN: swap NaN by difference in chainage i and i+1. This is possible becasue they are roads and not bridges. Bridges doesn't contain Nan values for length.
#print(merge_inner['chainage_x'].isna().sum()) # 924 missing values
#print(merge_inner['chainage_y'].isna().sum()) # No missing values!
#print(merge_inner['type_x'].isna().sum()) # 924 missing values
#print(merge_inner['name_x'].isna().sum()) # 924 missing values
#print(merge_inner['type_y'].isna().sum()) # No missing values!
#print(merge_inner['name_y'].isna().sum()) # No missing values
#print(merge_inner.length[2]) # both possible
#print(merge_inner.loc[2,'length']) # Both possible

for i in range(len(merge_inner['length'])-1): #when length is nan, take difference in chainage
    if np.isnan(merge_inner.loc[i,'length']) == True:
        merge_inner.loc[i,'length'] = (merge_inner.chainage_y[i+1] - merge_inner.chainage_y[i])

merge_inner = merge_inner[['road','LRPName','length','chainage_y','lon_y','lat_y','type_y','name_y','condition']] #only necessary columns.
print(merge_inner)

merge_inner.to_csv(r"C:\Github\epa1352advancedsimulation\assignment_2\EPA1352-G13-A2\data\demo_try_self.csv",index=False)