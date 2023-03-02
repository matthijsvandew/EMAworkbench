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

for i in df_roads['road']:
    i.strip()
for i in df_bmms['road']:
    i.strip()
for i in df_roads['LRPName']:
    i.strip()
for i in df_bmms['LRPName']:
    i.strip()

df_roads['LRPName'].str.strip()
df_bmms['LRPName'].str.strip()

merge_inner = df_bmms.merge(df_roads, how = 'inner',on=['LRPName','road'])

print(merge_inner)
