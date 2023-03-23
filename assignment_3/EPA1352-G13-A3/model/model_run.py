from model import BangladeshModel
from try_nx import road_network
import pandas as pd
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

use_random_seed = True

file = '../data\input_data6.csv'
network = road_network(file_name=file)
shortest_routes_sourcesinks = network.find_shortest_path()

for sce in range(5): ### Five different scenarios
    ### Initiate an empty dataframe. We will store all data for a single scenario over all replications there
    df_combined_sce = pd.DataFrame()
    for rep in range(1,11): ### Ten replications per scenario
        if use_random_seed == True: ### If we want to use a random seed: use random seed, otherwise seed 1234567
            seed = random.seed()
        else:
            seed = 1234567
        ### Initiate model
        sim_model = BangladeshModel(shortest_routes_sourcesinks, seed=seed,file = file,scenario=sce,replication=rep)
        for i in range(run_length): ### Run model as long as the run_length
            if i % 100 == 0:
                print(f'At step {i} for replication {rep} for scenario {sce}')
            sim_model.step()
        print(f'Finished replication {rep} for scenario {sce}')
        ### Append the data that is generated in the replication to the dataframe of the scenario (which contains replications)
        df_combined_sce = pd.concat([df_combined_sce,sim_model.save_results()])

        ### The following 2 lines can be used if you want to store data for each replication individually
        #df_single_rep_sce  = sim_model.save_results
        #df_single_rep_sce.to_csv(f'../experiment\scenario{sce}_replication_{rep}.csv')

    if sce == 0: ### Call scenario 0 the base case and store it
        df_combined_sce.to_csv(r'../experiment\base_case_results.csv', index_label='index')
    else: ### The rest of the scenario's will store their data based on the scenario number
        df_combined_sce.to_csv(f'../experiment\scenario{sce}_results.csv', index_label='index')
