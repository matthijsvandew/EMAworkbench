import pandas as pd
import numpy as np
import random

df_roads = pd.read_csv(r'C:\Github\epa1352advancedsimulation\assignment_2\WBSIM_Lab1_cleanedDataset\infrastructure\_roads3.csv')
df_bmms = pd.read_excel('BMMS_overview.xlsx')

df_bmms = df_bmms.drop(df_bmms[df_bmms['road'] != 'N1'].index)
df_roads = df_roads.drop(df_roads[df_roads['road'] != 'N1'].index)

for i in range(len(df_roads['chainage'])): #chainage omzetten naar meters, want dat is lengte ook.
     df_roads.loc[i,'chainage'] = (df_roads.loc[i,'chainage'] * 1000)

df_roads = df_roads.drop(df_roads[df_roads['gap'] == 'BE'].index)

df_roads = df_roads.drop(columns='gap')

df_roads = df_roads.rename(columns={'lrp':'LRPName'})
df_bmms = df_bmms.drop_duplicates(subset=['LRPName'])

merge_right = df_bmms.merge(df_roads, how = 'right',on=['LRPName','road'])

for i in range(len(merge_right['length'])-1): #when length is nan, take difference in chainage
    if np.isnan(merge_right.loc[i,'length']) == True:
        merge_right.loc[i,'length'] = (merge_right.chainage_y[i+1] - merge_right.chainage_y[i])

merge_right = merge_right[['road','LRPName','length','chainage_y','lon_y','lat_y','type_y','name_y','condition']] #only necessary columns.

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

Total_count = CountA + CountB + CountC + CountD
Count_BCD = CountB + CountC + CountD
Count_CD = CountC + CountD

Fraction_A_total = CountA / Total_count
Fraction_B_BCD = CountB / Count_BCD
Fraction_C_CD = CountC / Count_CD

a = random.random()
b = random.random()
c = random.random()

for i in range(len(merge_right['condition'])):
     if merge_right.loc[i, 'type_y'] == 'Culvert' or merge_right.loc[i, 'type_y'] == 'Bridge':
          if pd.isna(merge_right.loc[i, 'condition']) == True:
               if a < Fraction_A_total:
                    merge_right.loc[i, 'condition'] = 'A'
               elif b < Fraction_B_BCD:
                    merge_right.loc[i, 'condition'] = 'B'
               elif c < Fraction_C_CD:
                    merge_right.loc[i, 'condition'] = 'C'
               else:
                    merge_right.loc[i, 'condition'] = 'D'

# count=0
# for i in range(len(merge_right['condition'])):
#      if merge_right.loc[i, 'type_y'] == 'Culvert' or merge_right.loc[i, 'type_y'] == 'Bridge':
#           if pd.isna(merge_right.loc[i, 'condition']) == True:
#                count+=1
# print(count)

merge_right.insert(loc=0,column='id',value=0)

for i in range(len(merge_right)):
     merge_right.loc[i, 'id'] = round(i)
     #print(i)
     #print(int(i))


for i in range(len(merge_right)):
     if i == 0:
          merge_right.loc[i, 'type_y'] = 'source'
     elif i == len(merge_right):
          merge_right.loc[i, 'type_y'] = 'sink'
     elif merge_right.loc[i, 'type_y'] == 'Culvert' or merge_right.loc[i, 'type_y'] == 'Bridge':
          merge_right.loc[i, 'type_y'] = 'bridge'
     else:
          merge_right.loc[i, 'type_y'] = 'link'

merge_right= merge_right.rename(columns={'type_y':'model_type','lat_y':'lat','lon_y':'lon','name_y':'name','chainage_y':'chainage'})

#merge_right.to_csv(r"C:\Github\epa1352advancedsimulation\assignment_2\EPA1352-G13-A2\data\demo_try_self3.csv",index=False)