import pandas as pd

from model import BangladeshModel
import random

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
run_length = 5 * 24 * 60

# run time 1000 ticks
#run_length = 1000

#seed = 1234567

df_combined_sce_rep = pd.DataFrame()

for sce in range(9): #eight different scenarios
    for rep in range(10): #ten replications per scenario
        scenario = sce
        seed = random.seed()
        sim_model = BangladeshModel(seed=seed,scenario=scenario,replication=rep,run_length_model=run_length)
        for i in range(run_length):
            sim_model.step()
        if i == run_length - 1:
            df_combined_sce_rep =df_combined_sce_rep.append(sim_model.save_results(), ignore_index=True)

df_combined_sce_rep.to_csv(r'C:\Github\epa1352advancedsimulation\assignment_2\EPA1352-G13-A2\experiment\experimental_output_combined.csv',index_label='index')