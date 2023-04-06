import pandas as pd

df_analysis_3 = pd.read_csv(r'../experiment\results_bridges\bridges_combined_results.csv')

print(df_analysis_3)

df_analysis_3.insert(loc=6,column='Part_of_road',value=0)

for i in range(len(df_analysis_3['id'])):
    if df_analysis_3.loc[i,'id'] <= 7 and df_analysis_3.loc[i,'id'] >= 0:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N1, LRPS - LRP009a'
    elif df_analysis_3.loc[i,'id'] <= 123 and df_analysis_3.loc[i,'id'] >= 7:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N1, LRP009a - LRP084a'
    elif df_analysis_3.loc[i,'id'] <= 294 and df_analysis_3.loc[i,'id'] >= 123:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N1, LRP084a - LRP184a'
    elif df_analysis_3.loc[i,'id'] <= 491 and df_analysis_3.loc[i,'id'] >= 294:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N1, LRP184a - LRP260c'
    elif df_analysis_3.loc[i,'id'] <= 559 and df_analysis_3.loc[i,'id'] >= 491:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N1, LRP260c - LRP293a'
    elif df_analysis_3.loc[i,'id'] <= 1298 and df_analysis_3.loc[i,'id'] >= 559:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N1, LRP293a - LRPE'
    elif df_analysis_3.loc[i,'id'] <= 1471 and df_analysis_3.loc[i,'id'] >= 1299:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N102, LRPS - LRPE'
    elif df_analysis_3.loc[i,'id'] <= 1563 and df_analysis_3.loc[i,'id'] >= 1472:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N104, LRP001a - LRPE'
    elif df_analysis_3.loc[i,'id'] <= 1588 and df_analysis_3.loc[i,'id'] >= 1564:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N105, LRPS - LRP012a'
    elif df_analysis_3.loc[i,'id'] <= 1669 and df_analysis_3.loc[i,'id'] >= 1588:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N105, LRP012a - LRP048'
    elif df_analysis_3.loc[i,'id'] <= 1897 and df_analysis_3.loc[i,'id'] >= 1672:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N106, LRP_insert - LRPE'
    elif df_analysis_3.loc[i,'id'] <= 1902 and df_analysis_3.loc[i,'id'] >= 1898:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N2, LRPS - LRP012a'
    elif df_analysis_3.loc[i,'id'] <= 2113 and df_analysis_3.loc[i,'id'] >= 1902:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N2, LRP012a - LRP086a'
    elif df_analysis_3.loc[i,'id'] <= 2186 and df_analysis_3.loc[i,'id'] >= 2113:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N2, LRP086a - LRP117b'
    elif df_analysis_3.loc[i,'id'] <= 2322 and df_analysis_3.loc[i,'id'] >= 2186:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N2, LRP117b - LRP146b'
    elif df_analysis_3.loc[i,'id'] <= 2585 and df_analysis_3.loc[i,'id'] >= 2322:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N2, LRP146b - LRP191b'
    elif df_analysis_3.loc[i,'id'] <= 2680 and df_analysis_3.loc[i,'id'] >= 2585:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N2, LRP191b - LRP228c'
    elif df_analysis_3.loc[i,'id'] <= 2691 and df_analysis_3.loc[i,'id'] >= 2680:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N2, LRP228c - LRP231b'
    elif df_analysis_3.loc[i,'id'] <= 2716 and df_analysis_3.loc[i,'id'] >= 2691:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N2, LRP231b - LRP239a'
    elif df_analysis_3.loc[i,'id'] <= 2817 and df_analysis_3.loc[i,'id'] >= 2716:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N2, LRP239a - LRPE'
    elif df_analysis_3.loc[i,'id'] <= 2908 and df_analysis_3.loc[i,'id'] >= 2817:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N204, LRPS - LRPE'
    elif df_analysis_3.loc[i,'id'] <= 3070 and df_analysis_3.loc[i,'id'] >= 2909:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N207, LRPS - LRPE'
    elif df_analysis_3.loc[i,'id'] <= 3257 and df_analysis_3.loc[i,'id'] >= 3071:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N208, LRPS - LRP054a'
    elif df_analysis_3.loc[i,'id'] <= 3261 and df_analysis_3.loc[i,'id'] >= 3257:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N208, LRP054a - LRPE'
    elif df_analysis_3.loc[i,'id'] <= 3311 and df_analysis_3.loc[i,'id'] >= 3262:
        df_analysis_3.loc[i, 'Part_of_road'] = 'N210, LRPS - LRPE'

#df_analysis_3.to_csv(r"../experiment\test_analysis.csv", index = False)

Delaytime_dict = {}
for i in range(len(df_analysis_3['id'])):
    Delaytime_dict[df_analysis_3.loc[i, 'id']] = []

for i in range(len(df_analysis_3['id'])):
    Delaytime_dict[df_analysis_3.loc[i, 'id']] += [df_analysis_3.loc[i, 'caused_delay_time']]

Average_delaytime_dict = {}
for i in Delaytime_dict:
    Average_delaytime_dict[i] = sum(Delaytime_dict[i])/len(Delaytime_dict[i])

print(Average_delaytime_dict)

df = pd.DataFrame.from_records(Average_delaytime_dict, index=['delay_time'])
df = df.transpose()

df = df.reset_index()
df = df.rename(columns={'index': 'bridge_id'})
#print(df)

df.delay_time.describe()
print(df.delay_time.describe())

#highest top 10
df.sort_values('delay_time',ascending=False,inplace=True)
print(df.head(10))

#lowest top10
df.sort_values('delay_time',ascending=True,inplace=True)
print(df.head(10))

#df.to_csv(r"../experiment\test_analysis1.csv", index = True)

sns.boxplot(data=df,x='delay_time', ax=ax[0,0], color='r').set(title= 'Boxplot driving time base scenario');

plt.show()