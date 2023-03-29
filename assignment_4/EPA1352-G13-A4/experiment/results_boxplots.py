import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Read in the output data of the different scenarios.
Base_scenario = pd.read_csv(r'../experiment\base_case_results.csv')
scenario_1_data = pd.read_csv(r'../experiment\scenario1_results.csv')
scenario_2_data = pd.read_csv(r'../experiment\scenario2_results.csv')
scenario_3_data = pd.read_csv(r'../experiment\scenario3_results.csv')
scenario_4_data = pd.read_csv(r'../experiment\scenario4_results.csv')

# Setup a plot.
fig , ax = plt.subplots(2,3, figsize=(17,10))

# Show the boxplots of the driving time over the different scenarios.
sns.boxplot(data=Base_scenario,x='drive_time', ax=ax[0,0], color='r').set(title= 'Boxplot driving time base scenario');
sns.boxplot(data=scenario_1_data,x='drive_time', ax=ax[0,1], color='r').set(title= 'Boxplot driving time scenario 1');
sns.boxplot(data=scenario_2_data,x='drive_time', ax=ax[0,2], color='r').set(title= 'Boxplot driving time scenario 2');
sns.boxplot(data=scenario_3_data,x='drive_time', ax=ax[1,0], color='r').set(title= 'Boxplot driving time scenario 3');
sns.boxplot(data=scenario_4_data,x='drive_time', ax=ax[1,1], color='r').set(title= 'Boxplot driving time scenario 4');

plt.show()