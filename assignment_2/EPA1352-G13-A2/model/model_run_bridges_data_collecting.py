import pandas as pd

from model import BangladeshModel
import random

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

### The long run length reflects the run that will be used for experimentation
### run time 5 x 24 hours x 60 minutes; 1 tick 1 minute
long_run_length = 5 * 24 * 60

### The short run length reflects a run that will be used for debugging because it is a lot faster.
short_run_length = 500

debug_run = False ### If we want to debug: use the shorter run length
if debug_run == True:
    run_length = short_run_length
else:
    run_length = long_run_length

### Similar to the shorter run length, a non-random seed is more useful for debugging.
use_random_seed = True

for sce in range(9): ### Nine different scenarios
    ### Initiate an empty dataframe. We will store all data for a single scenario over all replications there
    df_combined_sce = pd.DataFrame()
    for rep in range(1,11): ### Ten replications per scenario
        if use_random_seed == True: ### If we want to use a random seed: use random seed, otherwise seed 123456789
            seed = random.seed()
        else:
            seed = 123456789
        ### Initiate model
        sim_model = BangladeshModel(seed=seed,scenario=sce,replication=rep,run_length_model=run_length)
        for i in range(run_length): ### Run model as long as the run_length
            sim_model.step()
        df_combined_sce =df_combined_sce.append(sim_model.save_results(), ignore_index=True)

    if sce == 0:
        df_combined_sce.to_csv(r'../experiment\base_case_results.csv', index_label='index')
    else:
        df_combined_sce.to_csv(f'../experiment\scenario{sce}_results.csv', index_label='index')