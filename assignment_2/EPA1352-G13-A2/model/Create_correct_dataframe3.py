import pandas as pd
import numpy as np

df_roads = pd.read_csv(r'C:\Github\epa1352advancedsimulation\assignment_2\WBSIM_Lab1_cleanedDataset\infrastructure\_roads3.csv')
#df_roads = df_roads.drop(columns='gap')
df_bmms = pd.read_excel('BMMS_overview.xlsx')

df_bmms = df_bmms.drop(df_bmms[df_bmms['road'] != 'N1'].index)
df_roads = df_roads.drop(df_roads[df_roads['road'] != 'N1'].index)

for i in range(len(df_roads['chainage'])): #chainage omzetten naar meters, want dat is lengte ook.
     df_roads.loc[i,'chainage'] = (df_roads.loc[i,'chainage'] * 1000)

df_roads = df_roads.drop(df_roads[df_roads['gap'] == 'BE'].index)

df_roads = df_roads.drop(columns='gap')

df_roads = df_roads.rename(columns={'lrp':'LRPName'})
df_bmms = df_bmms.drop_duplicates(subset=['LRPName'])
df_roads = df_roads.rename(columns={'lrp':'LRPName'})



merge_right = df_bmms.merge(df_roads, how = 'right',on=['LRPName','road'])

for i in range(len(merge_right['length'])-1): #when length is nan, take difference in chainage
    if np.isnan(merge_right.loc[i,'length']) == True:
        merge_right.loc[i,'length'] = (merge_right.chainage_y[i+1] - merge_right.chainage_y[i])

merge_right = merge_right[['road','LRPName','length','chainage_y','lon_y','lat_y','type_y','name_y','condition']] #only necessary columns.
print(merge_right)

CountA = 0
CountB = 0
CountC = 0
CountD = 0

for i in range(len(merge_right['condition'])-1):
     if merge_right.loc[i, 'condition'] == 'A':
          CountA = CountA + 1
     elif merge_right.loc[i, 'condition'] == 'B':
          CountB = CountB + 1
     elif merge_right.loc[i, 'condition'] == 'C':
          CountC = CountC + 1
     elif merge_right.loc[i, 'condition'] == 'D':
          CountD = CountD + 1
     elif np.isnan(merge_right.loc[i, 'condition']) == True:
          continue

total_count = CountA + CountB + CountC + CountD
# print(CountA)
# print(CountB)
# print(CountC)
# print(CountD)
# print(total_count)
fraction_A = CountA / total_count
fraction_B = CountB / total_count
fraction_C = CountD / total_count
fraction_D = CountD / total_count

#merge_right.to_csv(r"C:\Github\epa1352advancedsimulation\assignment_2\EPA1352-G13-A2\data\demo_try_self2.csv",index=False)