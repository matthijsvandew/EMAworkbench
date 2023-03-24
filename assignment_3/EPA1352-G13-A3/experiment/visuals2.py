import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

Base_scenario = pd.read_csv(r'../experiment\base_case_results.csv')
scenario_1_data = pd.read_csv(r'../experiment\scenario1_results.csv')
scenario_2_data = pd.read_csv(r'../experiment\scenario2_results.csv')
scenario_3_data = pd.read_csv(r'../experiment\scenario3_results.csv')
scenario_4_data = pd.read_csv(r'../experiment\scenario4_results.csv')

Base_scenario_drive = Base_scenario['drive_time']
scenario_1_data_drive = scenario_1_data['drive_time']
scenario_2_data_drive = scenario_2_data['drive_time']
scenario_3_data_drive = scenario_3_data['drive_time']
scenario_4_data_drive = scenario_4_data['drive_time']

Base_scenario_drive.describe()
print(Base_scenario_drive.describe())

scenario_1_data_drive.describe()
print(scenario_1_data_drive.describe())

scenario_2_data_drive.describe()
print(scenario_2_data_drive.describe())

scenario_3_data_drive.describe()
print(scenario_3_data_drive.describe())

scenario_4_data_drive.describe()
print(scenario_4_data_drive.describe())
