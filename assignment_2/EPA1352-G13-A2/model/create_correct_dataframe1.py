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

merge = df_bmms.merge(df_roads, how = 'outer',on=['LRPName','road'])
print(merge)
print(merge.columns)
print(merge.head(10))

print(merge.loc[2,:])
print(merge.loc[3,:]) #er zit spatie achter die LRP008b, daarom herkent ie m niet en staat ie er dubbel in! White space verwijderen proberen.
