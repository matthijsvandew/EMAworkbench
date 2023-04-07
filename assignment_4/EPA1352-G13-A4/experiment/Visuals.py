import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

scenario_1_data = pd.read_csv(r'../experiment\results_bridges\bridges_scenario1_results.csv')
scenario_2_data = pd.read_csv(r'../experiment\results_bridges\bridges_scenario2_results.csv')
scenario_3_data = pd.read_csv(r'../experiment\results_bridges\bridges_scenario3_results.csv')
scenario_4_data = pd.read_csv(r'../experiment\results_bridges\bridges_scenario4_results.csv')
scenario_5_data = pd.read_csv(r'../experiment\results_bridges\bridges_scenario5_results.csv')
scenario_6_data = pd.read_csv(r'../experiment\results_bridges\bridges_scenario6_results.csv')
scenario_7_data = pd.read_csv(r'../experiment\results_bridges\bridges_scenario7_results.csv')
scenario_8_data = pd.read_csv(r'../experiment\results_bridges\bridges_scenario8_results.csv')
scenario_8_30_data = pd.read_csv(r'../experiment\results_bridges\bridges_scenario_8_30_results.csv')

fig , ax = plt.subplots(3,3, figsize=(17,10))


sns.boxplot(data=scenario_1_data,x='caused_delay_time', ax=ax[0,0], color='r').set(title= 'Boxplot delay time scenario 1');
sns.boxplot(data=scenario_2_data,x='caused_delay_time', ax=ax[0,1], color='r').set(title= 'Boxplot delay time scenario 2');
sns.boxplot(data=scenario_3_data,x='caused_delay_time', ax=ax[0,2], color='r').set(title= 'Boxplot delay time scenario 3');
sns.boxplot(data=scenario_4_data,x='caused_delay_time', ax=ax[1,0], color='r').set(title= 'Boxplot delay time scenario 4');
sns.boxplot(data=scenario_5_data,x='caused_delay_time', ax=ax[1,1], color='r').set(title= 'Boxplot delay time scenario 5');
sns.boxplot(data=scenario_6_data,x='caused_delay_time', ax=ax[1,2], color='r').set(title= 'Boxplot delay time scenario 6');
sns.boxplot(data=scenario_7_data,x='caused_delay_time', ax=ax[2,0], color='r').set(title= 'Boxplot delay time scenario 7');
sns.boxplot(data=scenario_8_data,x='caused_delay_time', ax=ax[2,1], color='r').set(title= 'Boxplot delay time scenario 8');
sns.boxplot(data=scenario_8_30_data,x='caused_delay_time', ax=ax[2,2], color='r').set(title= 'Boxplot delay time scenario 8_30');

plt.show()