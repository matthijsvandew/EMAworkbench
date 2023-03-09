import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

Base_scenario = pd.read_csv(r'../experiment\base_case_results.csv')
scenario_1_data = pd.read_csv(r'../experiment\scenario1_results.csv')
scenario_2_data = pd.read_csv(r'../experiment\scenario2_results.csv')
scenario_3_data = pd.read_csv(r'../experiment\scenario3_results.csv')
scenario_4_data = pd.read_csv(r'../experiment\scenario4_results.csv')
scenario_5_data = pd.read_csv(r'../experiment\scenario5_results.csv')
scenario_6_data = pd.read_csv(r'../experiment\scenario6_results.csv')
scenario_7_data = pd.read_csv(r'../experiment\scenario7_results.csv')
scenario_8_data = pd.read_csv(r'../experiment\scenario8_results.csv')

fig , ax = plt.subplots(3,3, figsize=(17,10))

sns.boxplot(data=Base_scenario,x='drive_time', ax=ax[0,0], color='r').set(title= 'Boxplot driving time base scenario');
sns.boxplot(data=scenario_1_data,x='drive_time', ax=ax[0,1], color='r').set(title= 'Boxplot driving time scenario 1');
sns.boxplot(data=scenario_2_data,x='drive_time', ax=ax[0,2], color='r').set(title= 'Boxplot driving time scenario 2');
sns.boxplot(data=scenario_3_data,x='drive_time', ax=ax[1,0], color='r').set(title= 'Boxplot driving time scenario 3');
sns.boxplot(data=scenario_4_data,x='drive_time', ax=ax[1,1], color='r').set(title= 'Boxplot driving time scenario 4');
sns.boxplot(data=scenario_5_data,x='drive_time', ax=ax[1,2], color='r').set(title= 'Boxplot driving time scenario 5');
sns.boxplot(data=scenario_6_data,x='drive_time', ax=ax[2,0], color='r').set(title= 'Boxplot driving time scenario 6');
sns.boxplot(data=scenario_7_data,x='drive_time', ax=ax[2,1], color='r').set(title= 'Boxplot driving time scenario 7');
sns.boxplot(data=scenario_8_data,x='drive_time', ax=ax[2,2], color='r').set(title= 'Boxplot driving time scenario 8');

plt.show()