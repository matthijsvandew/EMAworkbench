import pandas as pd
import numpy as np
import random

df_roads = pd.read_csv(r'../data\_roads3.csv')
df_bmms = pd.read_excel('../data\BMMS_overview.xlsx')

df_bmms = df_bmms.drop(df_bmms[df_bmms['road'] != 'N1'].index)
df_roads = df_roads.drop(df_roads[df_roads['road'] != 'N1'].index)

#These lines of codes could be used in order to delete 'Left bridges' out of the data set for this specific assignment.
#However, this is not representitive when this model would be applied for more than just one route and, therefore, this line of code is shown in markdown format.
#This subject is further explained in the discussion of the report.
# df_bmms = df_bmms[df_bmms["name"].str.contains("(L)") == False]
# df_bmms = df_bmms[df_bmms["name"].str.contains("( L )") == False]


for i in range(len(df_roads['chainage'])): #chainage omzetten naar meters, want dat is lengte ook.
     df_roads.loc[i,'chainage'] = (df_roads.loc[i,'chainage'] * 1000)

df_roads = df_roads.drop(df_roads[df_roads['gap'] == 'BE'].index)

df_roads = df_roads.drop(columns='gap')

df_roads = df_roads.rename(columns={'lrp':'LRPName'})
df_bmms = df_bmms.drop_duplicates(subset=['LRPName'])

merge_right = df_bmms.merge(df_roads, how = 'right',on=['LRPName','road'])

#Check which one must be selected for the final dataset
#print(merge_right['lon_y'].isna().sum()) # No missing values!
#print(merge_right['lon_x'].isna().sum()) # 924 missing values!
#print(merge_right['lat_y'].isna().sum()) # No missing values!
#print(merge_right['lat_x'].isna().sum()) # 924 missing values
#print(merge_right['length'].isna().sum()) # 924 missing values. --> Must be fixed. solution: if length == NaN: swap NaN by difference in chainage i and i+1. This is possible becasue they are roads and not bridges. Bridges doesn't contain Nan values for length.
#print(merge_right['chainage_x'].isna().sum()) # 924 missing values
#print(merge_right['chainage_y'].isna().sum()) # No missing values!
#print(merge_right['type_x'].isna().sum()) # 924 missing values
#print(merge_right['name_x'].isna().sum()) # 924 missing values
#print(merge_right['type_y'].isna().sum()) # No missing values!
#print(merge_right['name_y'].isna().sum()) # No missing values
#print(merge_right.length[2]) # both possible
#print(merge_right.loc[2,'length']) # Both possible

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

merge_right = merge_right.loc[merge_right['id'] <= 502]

# for i in range(len(merge_right)):
#      #Start at Chittagong
#      if i == len(merge_right)-1:
#           merge_right.loc[i, 'type_y'] = 'source'
#      #End in Dhaka
#      elif i == 0:
#           merge_right.loc[i, 'type_y'] = 'sink'
#      elif merge_right.loc[i, 'type_y'] == 'Culvert' or merge_right.loc[i, 'type_y'] == 'Bridge':
#           merge_right.loc[i, 'type_y'] = 'bridge'
#      else:
#           merge_right.loc[i, 'type_y'] = 'link'
#
# merge_right= merge_right.rename(columns={'type_y':'model_type','lat_y':'lat','lon_y':'lon','name_y':'name','chainage_y':'chainage'})
#
# merge_right.to_csv(r"../data\input_data_n1.csv",index=False)