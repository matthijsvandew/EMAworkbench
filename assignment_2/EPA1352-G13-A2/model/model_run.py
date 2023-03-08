import pandas as pd

from model import BangladeshModel
import random

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours x 60 minutes; 1 tick 1 minute
long_run_length = 5 * 24 * 60

short_run_length = 500

short_run = False
if short_run == True:
    run_length = short_run_length
else:
    run_length = long_run_length

use_random_seed = True

df_combined_sce_rep = pd.DataFrame()

for sce in range(9): #nine different scenarios
    for rep in range(1,11): #ten replications per scenario
        scenario = sce
        if use_random_seed == True:
            seed = random.seed()
        else:
            seed = 123456789
        sim_model = BangladeshModel(seed=seed,scenario=scenario,replication=rep,run_length_model=run_length)
        for i in range(run_length):
            sim_model.step()
        if i == run_length - 1:
            df_combined_sce_rep =df_combined_sce_rep.append(sim_model.save_results(), ignore_index=True)

#df_combined_sce_rep.to_csv(r'C:\Github\epa1352advancedsimulation\assignment_2\EPA1352-G13-A2\experiment\experimental_output_combined.csv',index_label='index')

scenario_check = df_combined_sce_rep.groupby(df_combined_sce_rep.scenario)
df_scenario_0 = scenario_check.get_group(0)
df_scenario_1 = scenario_check.get_group(1)
df_scenario_2 = scenario_check.get_group(2)
df_scenario_3 = scenario_check.get_group(3)
df_scenario_4 = scenario_check.get_group(4)
df_scenario_5 = scenario_check.get_group(5)
df_scenario_6 = scenario_check.get_group(6)
df_scenario_7 = scenario_check.get_group(7)
df_scenario_8 = scenario_check.get_group(8)


df_scenario_0.to_csv(r'C:\Github\epa1352advancedsimulation\assignment_2\EPA1352-G13-A2\experiment\Base_case.csv',index_label='index')
df_scenario_1.to_csv(r'C:\Github\epa1352advancedsimulation\assignment_2\EPA1352-G13-A2\experiment\Scenario1.csv',index_label='index')
df_scenario_2.to_csv(r'C:\Github\epa1352advancedsimulation\assignment_2\EPA1352-G13-A2\experiment\Scenario2.csv',index_label='index')
df_scenario_3.to_csv(r'C:\Github\epa1352advancedsimulation\assignment_2\EPA1352-G13-A2\experiment\Scenario3.csv',index_label='index')
df_scenario_4.to_csv(r'C:\Github\epa1352advancedsimulation\assignment_2\EPA1352-G13-A2\experiment\Scenario4.csv',index_label='index')
df_scenario_5.to_csv(r'C:\Github\epa1352advancedsimulation\assignment_2\EPA1352-G13-A2\experiment\Scenario5.csv',index_label='index')
df_scenario_6.to_csv(r'C:\Github\epa1352advancedsimulation\assignment_2\EPA1352-G13-A2\experiment\Scenario7.csv',index_label='index')
df_scenario_8.to_csv(r'C:\Github\epa1352advancedsimulation\assignment_2\EPA1352-G13-A2\experiment\Scenario8.csv',index_label='index')
