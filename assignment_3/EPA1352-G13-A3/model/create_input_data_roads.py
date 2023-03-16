import pandas as pd
import numpy as np
import random

df_roads = pd.read_csv(r'../data\_roads3.csv')
df_bmms = pd.read_excel('../data\BMMS_overview.xlsx')

for i in range(len(df_roads['chainage'])): #chainage omzetten naar meters, want dat is lengte ook.
     df_roads.loc[i,'chainage'] = (df_roads.loc[i,'chainage'] * 1000)

df_roads = df_roads.drop(df_roads[df_roads['gap'] == 'BE'].index)

df_roads = df_roads.drop(columns='gap')

df_roads = df_roads.rename(columns={'lrp':'LRPName'})
df_bmms = df_bmms.drop_duplicates(subset=['LRPName'])

merge_right = df_bmms.merge(df_roads, how = 'right',on=['LRPName','road'])

merge_right = merge_right[(merge_right["road"].str.contains("N1") == True) | (merge_right["road"].str.contains("N2") == True)]

for i in range(len(merge_right['length'])-1): #when length is nan, take difference in chainage
    if np.isnan(merge_right.loc[i, 'length']) == True:
        merge_right.loc[i,'length'] = (merge_right.chainage_y[i+1] - merge_right.chainage_y[i])

merge_right = merge_right[['road','LRPName','length','chainage_y','lon_y','lat_y','type_y','name_y','condition']] #only necessary columns.

for i in range(len(merge_right['road'])-1):
    if merge_right.loc[i, 'road'] != merge_right.loc[i+1, 'road']:
        type_road = merge_right.loc[i, 'road']
        length_road = merge_right.chainage_y[i]
        if length_road < 25000:
             merge_right = merge_right.drop(merge_right[merge_right['road'] == type_road].index)

merge_right = merge_right.reset_index(drop=True)

CountA = 0
CountB = 0
CountC = 0
CountD = 0

for j in range(len(merge_right['condition'])-1):
     if merge_right.loc[j, 'condition'] == 'A':
          CountA = CountA + 1
     elif merge_right.loc[j, 'condition'] == 'B':
          CountB = CountB + 1
     elif merge_right.loc[j, 'condition'] == 'C':
          CountC = CountC + 1
     elif merge_right.loc[j, 'condition'] == 'D':
          CountD = CountD + 1
     elif np.isnan(merge_right.loc[j, 'condition']) == True:
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

merge_right.insert(loc=0,column='id',value=0)

for i in range(len(merge_right)):
     merge_right.loc[i, 'id'] = round(i)

for i in range(len(merge_right)):
     if i == len(merge_right)-1:
          merge_right.loc[i, 'type_y'] = 'sourcesink'
     elif i == 0:
          merge_right.loc[i, 'type_y'] = 'sourcesink'
     elif merge_right.loc[i, 'type_y'] == 'Culvert' or merge_right.loc[i, 'type_y'] == 'Bridge':
          merge_right.loc[i, 'type_y'] = 'bridge'
     else:
          merge_right.loc[i, 'type_y'] = 'link'
     if 'Intersect' in merge_right.loc[i, 'name_y'] and ('N1' or 'N2' in merge_right.loc[i, 'type_y']):
          merge_right.loc[i, 'type_y'] = 'intersection'
     if (merge_right.loc[i, 'type_y'] == 'CrossRoad') and ('N1' or 'N2' in merge_right.loc[i, 'type_y']):
          merge_right.loc[i, 'type_y'] = 'intersection'

for i in range(len(merge_right)-1):
     if merge_right.loc[i, 'road'] != merge_right.loc[i + 1, 'road']:
          merge_right.loc[i,'type_y'] = 'sourcesink'

merge_right= merge_right.rename(columns={'type_y':'model_type','lat_y':'lat','lon_y':'lon','name_y':'name','chainage_y':'chainage'})

for i in range(len(merge_right)-1):
     if merge_right.loc[i, 'model_type'] == 'bridge' and merge_right.loc[i+1, 'model_type'] == 'bridge':
          merge_right.loc[(i+0.5)] = [(i+1), merge_right.road[i], 'LRP_inserted', 0, 0, ((merge_right.lon[i] + merge_right.lon[i+1])/2), ((merge_right.lat[i] + merge_right.lat[i+1])/2), 'link', 'inserted_link', 'NaN']

merge_right = merge_right.sort_index().reset_index(drop=True)


for i in range(0, len(merge_right)-1):
     if i == len(merge_right):
          break
     if merge_right.loc[i, 'model_type'] == 'link':
          start_link = i
          while merge_right.loc[i+1, 'model_type'] == 'link':
               merge_right.length[start_link] = merge_right.length[start_link] + merge_right.length[i+1]
               merge_right = merge_right.drop([i+1])
               i = i+1
          merge_right = merge_right.reset_index(drop=True)

merge_right = merge_right.drop(columns=['id'])

merge_right.insert(loc=0,column='id',value=0)

for i in range(len(merge_right)):
     merge_right.loc[i, 'id'] = round(i)

merge_right.to_csv(r"../data\input_data_roads_test.csv", index_label='id')