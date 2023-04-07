import pandas as pd
import math

df_analysis = pd.read_csv(r'../experiment\results_bridges\bridges_scenario3_results.csv')

#print(df_analysis.head())


Delaytime_dict = {}
for i in range(len(df_analysis['id'])):
    Delaytime_dict[df_analysis.loc[i, 'id']] = []

for i in range(len(df_analysis['id'])):
    Delaytime_dict[df_analysis.loc[i, 'id']] += [df_analysis.loc[i, 'caused_delay_time']]

#print(Delaytime_dict)

Average_delaytime_dict = {}
for i in Delaytime_dict:
    Average_delaytime_dict[i] = sum(Delaytime_dict[i])/len(Delaytime_dict[i])

#print(Average_delaytime_dict)

df_delaytime = pd.DataFrame.from_records(Average_delaytime_dict, index=['delay_time'])
df_delaytime = df_delaytime.transpose()

df_delaytime = df_delaytime.reset_index()
df_delaytime = df_delaytime.rename(columns={'index': 'bridge_id'})
#print(df)



Number_of_trucks_dict = {}
for i in range(len(df_analysis['id'])):
    Number_of_trucks_dict[df_analysis.loc[i, 'id']] = []

for i in range(len(df_analysis['id'])):
    Number_of_trucks_dict[df_analysis.loc[i, 'id']] += [df_analysis.loc[i, 'number_of_vehicles']]

#print(Number_of_trucks_dict)
#print(Delaytime_dict)

Average_trucks_dict = {}
for i in Number_of_trucks_dict:
    Average_trucks_dict[i] = sum(Number_of_trucks_dict[i])/len(Number_of_trucks_dict[i])

#print(Average_trucks_dict)

df_trucks = pd.DataFrame.from_records(Average_trucks_dict, index=['number_of_vehicles'])
df_trucks = df_trucks.transpose()

df_trucks = df_trucks.reset_index()
df_trucks = df_trucks.rename(columns={'index': 'bridge_id'})
df_trucks.number_of_vehicles = df_trucks.number_of_vehicles.round()
#print(df_trucks.head())

df_merged = df_trucks.merge(df_delaytime, how = 'right',on=['bridge_id'])
#print(df_merged.head(5))

#highest top3
df_merged.sort_values('delay_time',ascending=False,inplace=True)
#print(df_merged.head(3))

#lowest top10
#df_merged.sort_values('delay_time',ascending=True,inplace=True)
#print(df_merged.head(10))

df_merged = df_merged.reset_index()
df_merged = df_merged.drop(columns='index')
df_merged.insert(loc=3,column='Part_of_road',value=0)

for i in range(len(df_merged['bridge_id'])):
    if df_merged.loc[i,'bridge_id'] <= 7 and df_merged.loc[i,'bridge_id'] >= 0:
        df_merged.loc[i, 'Part_of_road'] = 'N1, LRPS - LRP009a'
    elif df_merged.loc[i,'bridge_id'] <= 123 and df_merged.loc[i,'bridge_id'] >= 7:
        df_merged.loc[i, 'Part_of_road'] = 'N1, LRP009a - LRP084a'
    elif df_merged.loc[i,'bridge_id'] <= 294 and df_merged.loc[i,'bridge_id'] >= 123:
        df_merged.loc[i, 'Part_of_road'] = 'N1, LRP084a - LRP184a'
    elif df_merged.loc[i,'bridge_id'] <= 491 and df_merged.loc[i,'bridge_id'] >= 294:
        df_merged.loc[i, 'Part_of_road'] = 'N1, LRP184a - LRP260c'
    elif df_merged.loc[i,'bridge_id'] <= 559 and df_merged.loc[i,'bridge_id'] >= 491:
        df_merged.loc[i, 'Part_of_road'] = 'N1, LRP260c - LRP293a'
    elif df_merged.loc[i,'bridge_id'] <= 1298 and df_merged.loc[i,'bridge_id'] >= 559:
        df_merged.loc[i, 'Part_of_road'] = 'N1, LRP293a - LRPE'
    elif df_merged.loc[i,'bridge_id'] <= 1471 and df_merged.loc[i,'bridge_id'] >= 1299:
        df_merged.loc[i, 'Part_of_road'] = 'N102, LRPS - LRPE'
    elif df_merged.loc[i,'bridge_id'] <= 1563 and df_merged.loc[i,'bridge_id'] >= 1472:
        df_merged.loc[i, 'Part_of_road'] = 'N104, LRP001a - LRPE'
    elif df_merged.loc[i,'bridge_id'] <= 1588 and df_merged.loc[i,'bridge_id'] >= 1564:
        df_merged.loc[i, 'Part_of_road'] = 'N105, LRPS - LRP012a'
    elif df_merged.loc[i,'bridge_id'] <= 1669 and df_merged.loc[i,'bridge_id'] >= 1588:
        df_merged.loc[i, 'Part_of_road'] = 'N105, LRP012a - LRP048'
    elif df_merged.loc[i,'bridge_id'] <= 1897 and df_merged.loc[i,'bridge_id'] >= 1672:
        df_merged.loc[i, 'Part_of_road'] = 'N106, LRP_insert - LRPE'
    elif df_merged.loc[i,'bridge_id'] <= 1902 and df_merged.loc[i,'bridge_id'] >= 1898:
        df_merged.loc[i, 'Part_of_road'] = 'N2, LRPS - LRP012a'
    elif df_merged.loc[i,'bridge_id'] <= 2113 and df_merged.loc[i,'bridge_id'] >= 1902:
        df_merged.loc[i, 'Part_of_road'] = 'N2, LRP012a - LRP086a'
    elif df_merged.loc[i,'bridge_id'] <= 2186 and df_merged.loc[i,'bridge_id'] >= 2113:
        df_merged.loc[i, 'Part_of_road'] = 'N2, LRP086a - LRP117b'
    elif df_merged.loc[i,'bridge_id'] <= 2322 and df_merged.loc[i,'bridge_id'] >= 2186:
        df_merged.loc[i, 'Part_of_road'] = 'N2, LRP117b - LRP146b'
    elif df_merged.loc[i,'bridge_id'] <= 2585 and df_merged.loc[i,'bridge_id'] >= 2322:
        df_merged.loc[i, 'Part_of_road'] = 'N2, LRP146b - LRP191b'
    elif df_merged.loc[i,'bridge_id'] <= 2680 and df_merged.loc[i,'bridge_id'] >= 2585:
        df_merged.loc[i, 'Part_of_road'] = 'N2, LRP191b - LRP228c'
    elif df_merged.loc[i,'bridge_id'] <= 2691 and df_merged.loc[i,'bridge_id'] >= 2680:
        df_merged.loc[i, 'Part_of_road'] = 'N2, LRP228c - LRP231b'
    elif df_merged.loc[i,'bridge_id'] <= 2716 and df_merged.loc[i,'bridge_id'] >= 2691:
        df_merged.loc[i, 'Part_of_road'] = 'N2, LRP231b - LRP239a'
    elif df_merged.loc[i,'bridge_id'] <= 2817 and df_merged.loc[i,'bridge_id'] >= 2716:
        df_merged.loc[i, 'Part_of_road'] = 'N2, LRP239a - LRPE'
    elif df_merged.loc[i,'bridge_id'] <= 2908 and df_merged.loc[i,'bridge_id'] >= 2817:
        df_merged.loc[i, 'Part_of_road'] = 'N204, LRPS - LRPE'
    elif df_merged.loc[i,'bridge_id'] <= 3070 and df_merged.loc[i,'bridge_id'] >= 2909:
        df_merged.loc[i, 'Part_of_road'] = 'N207, LRPS - LRPE'
    elif df_merged.loc[i,'bridge_id'] <= 3257 and df_merged.loc[i,'bridge_id'] >= 3071:
        df_merged.loc[i, 'Part_of_road'] = 'N208, LRPS - LRP054a'
    elif df_merged.loc[i,'bridge_id'] <= 3261 and df_merged.loc[i,'bridge_id'] >= 3257:
        df_merged.loc[i, 'Part_of_road'] = 'N208, LRP054a - LRPE'
    elif df_merged.loc[i,'bridge_id'] <= 3311 and df_merged.loc[i,'bridge_id'] >= 3262:
        df_merged.loc[i, 'Part_of_road'] = 'N210, LRPS - LRPE'

print(df_merged.head())

df_merged.to_csv(r"../experiment\Analysed_results_bridges\Results_scenario3.csv", index = True)

