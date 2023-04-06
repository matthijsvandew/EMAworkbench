import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df_all = pd.read_csv(r'../experiment\results_bridges\bridges_combined_results.csv')
df_1 = pd.read_csv(r'../experiment\results_bridges\bridges_scenario1_results.csv')
df_2 = pd.read_csv(r'../experiment\results_bridges\bridges_scenario2_results.csv')
df_3 = pd.read_csv(r'../experiment\results_bridges\bridges_scenario3_results.csv')
df_4 = pd.read_csv(r'../experiment\results_bridges\bridges_scenario4_results.csv')

# Setup a plot.
#fig , ax = plt.subplots(3,2, figsize=(10,10))

# Show the boxplots of the driving time over the different scenarios.
#sns.boxplot(data=df_all,x='caused_delay_time', ax=ax[0,0], color='r').set(title= 'Bridges delay times all scenarios');
#sns.boxplot(data=df_1,x='caused_delay_time', ax=ax[0,1], color='r').set(title= 'Bridges delay times scenario 1');
#sns.boxplot(data=df_2,x='caused_delay_time', ax=ax[1,0], color='r').set(title= 'Bridges delay times scenario 2');
#sns.boxplot(data=df_3,x='caused_delay_time', ax=ax[1,1], color='r').set(title= 'Bridges delay times scenario 3');
#sns.boxplot(data=df_4 ,x='caused_delay_time', ax=ax[2,0], color='r').set(title= 'Bridges delay times scenario 4');
#plt.show()

#df_all.caused_delay_time.describe()
#print(df_all.caused_delay_time.describe())

#df_1.caused_delay_time.describe()
#print(df_1.caused_delay_time.describe())

#df_2.caused_delay_time.describe()
#print(df_2.caused_delay_time.describe())

#df_3.caused_delay_time.describe()
#print(df_3.caused_delay_time.describe())

#df_4.caused_delay_time.describe()
#print(df_4.caused_delay_time.describe())

df_all.sort_values('caused_delay_time',ascending=False,inplace=True)
print(df_all.head(10))

df_1.sort_values('caused_delay_time',ascending=False,inplace=True)
print(df_1.head(10))

df_2.sort_values('caused_delay_time',ascending=False,inplace=True)
print(df_2.head(10))

df_3.sort_values('caused_delay_time',ascending=False,inplace=True)
print(df_3.head(10))

df_4.sort_values('caused_delay_time',ascending=False,inplace=True)
print(df_4.head(10))