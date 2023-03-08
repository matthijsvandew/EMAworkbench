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

for sce in range(1,2): #eight different scenarios
    for rep in range(1,3): #ten replications per scenario
        scenario = sce
        seed = random.seed()
        sim_model = BangladeshModel(seed=seed,scenario=scenario,replication=rep,run_length_model=run_length)
        for i in range(run_length):
            #print(i)
            sim_model.step()
        if i == run_length - 1:
            df_combined_sce_rep =df_combined_sce_rep.append(sim_model.save_results(), ignore_index=True)

df_combined_sce_rep.to_csv(f'C:\Github\epa1352advancedsimulation\data_assignment_2\combined.csv')


# Check if the seed is set
#print("SEED " + str(sim_model._seed))

# One run with given steps
#for i in range(run_length):
    #sim_model.step()
