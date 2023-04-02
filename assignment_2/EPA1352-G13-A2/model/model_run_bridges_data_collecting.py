import pandas as pd
from model_bridges_data_collecting import BangladeshModel
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

for sce in range(9): ### Nine scenarios
    ### Initiate an empty dataframe. We will store all data for a single scenario over all replications there
    df_bridges_combined = pd.DataFrame()
    for rep in range(1,11): ### Ten replications per scenario. Excel is only able to display around four scenarios. The number of rows are too large. See discussion in repport for an ellaboration on this.
        print('scenario',sce,'','replication', rep)
        if use_random_seed == True: ### If we want to use a random seed: use random seed, otherwise seed 123456789
            seed = random.seed()
        else:
            seed = 123456789
        ### Initiate model
        sim_model = BangladeshModel(seed=seed,scenario=sce,replication=rep)
        for i in range(run_length): ### Run model as long as the run_length
            sim_model.step()
        df_bridges_combined = df_bridges_combined.append(sim_model.bridge_save_results(), ignore_index=True)
        #df_bridges_combined = pd.concat(df_bridges_combined, sim_model.bridge_save_results())

    if sce == 0:
        df_bridges_combined.to_csv(r'../experiment\base_case_bridge_results.csv', index_label='index')
    else:
        df_bridges_combined.to_csv(f'../experiment\scenario{sce}_bridge_results.csv', index_label='index')