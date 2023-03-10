import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


scenario_8_data_bridges = pd.read_csv(r'../experiment\scenario8_bridge_results.csv')
scenario_8_data_bridges = scenario_8_data_bridges.groupby('id')['caused_delay_time'].sum().reset_index()
print(scenario_8_data_bridges)
fig , ax = plt.subplots(1,1)


sns.boxplot(data=scenario_8_data_bridges,x='caused_delay_time', ax=ax, color='r').set(title= 'Boxplot delay time due to bridges scenario 8');

plt.show()