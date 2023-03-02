import pandas as pd
#pip install --force-reinstall -v "openpyxl==3.1.0"

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

print(merge_inner)
print(len(merge_inner))
print(merge_inner.columns)

print(merge_inner['lon_y'].isna().sum())
print(merge_inner['lon_x'].isna().sum()) #924 missing values!
print(merge_inner['lat_y'].isna().sum())
print(merge_inner['lat_y'].isna().sum())
print(merge_inner['length'].isna().sum()) #924 missing values. Voor missing values length oplossing: als length == NaN: vervang NaN door verschil chainage i en i+1. Dat kan omdat dit roads zijn en geen bridges. Voor bridges is namelijk geen NaN value bij length.
print(merge_inner['chainage_x'].isna().sum()) #924 missing values
print(merge_inner['chainage_y'].isna().sum())