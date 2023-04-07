from model import BangladeshModel
from road_graph_nx import road_graph
import pandas as pd
import random
from datetime import datetime

import simulator

def main():
    """
        Run simulation
        Print output at terminal
    """
    # ---------------------------------------------------------------
    # Run settings:

    debug_run = False  # If we want to debug: use the shorter run length.
    multiprocessing = True # Run on multiple cores or on single-core
    random_seed = True # Use a random seed or with a static seed
    file = '../data\input_data.csv' # Use this input file for the road network for the simulation

    # ---------------------------------------------------------------
    # Simulate:

    start_time = datetime.now() # To keep track of run time

    print("The start time of the simulation =", start_time)

    run_settings_dict = {}

    # The long run length reflects the run that will be used for experimentation.
    # run time 5 x 24 hours x 60 minutes; 1 tick 1 minute.
    long_run_length = 5 * 24 * 60

    # The short run length reflects a run that will be used for debugging because it is a lot faster.
    short_run_length = 500

    if debug_run == True:
        run_settings_dict['run_length'] = short_run_length
    else:
        run_settings_dict['run_length'] = long_run_length

    run_settings_dict['file'] = file

    run_settings_dict['random-seed'] = random_seed

   # run_settings_dict['shortest_routes_sourcesinks'] = road_graph.find_shortest_path(file_name=file) # Find the shortest paths from every node to every other node in the network.
                                                                                # Call the find_shortest_path in the road_graph class, which are in the road_graph_nx.py file.

    sce_rep_dict = {}

    for sce in range(0,9): # Ten different scenarios.
        # Initiate an empty dataframe. We will store all data for a single scenario over all replications there.
        for rep in range(1,11): # Ten replications per scenario.
            sce_rep_dict[(sce, rep)] = run_settings_dict

    if multiprocessing == True: # Run the model on multi-threading
        results_df_combined_trucks, results_df_combined_bridges  = simulator.perform_multi_threading(sce_rep_dict)
    else:
        results_df_combined_trucks, results_df_combined_bridges  = simulator.perform_single_threading(sce_rep_dict)

    scenarios = results_df_combined_bridges['scenario'].unique()
    for sce in scenarios:
        if sce == 0: # Scenario 0 will be caved as the base-case
           # results_df_combined_trucks.loc[results_df_combined_trucks['scenario'] == 0].to_csv\
              #  (r'../experiment\results_trucks\trucks_base_case_results.csv', index_label='index', index=False)
            results_df_combined_bridges.loc[results_df_combined_bridges['scenario'] == 0].to_csv \
                (r'../experiment\results_bridges\bridges_base_case_results.csv', index_label='index', index=False)
        else: # Other scenarios will be saved by their scenario number
            #results_df_combined_trucks.loc[results_df_combined_trucks['scenario'] == sce].to_csv \
              #  (f'../experiment\\results_trucks\\trucks_scenario{sce}_results.csv', index_label='index', index=False)
            results_df_combined_bridges.loc[results_df_combined_bridges['scenario'] == sce].to_csv \
                (f'../experiment\\results_bridges\\bridges_scenario{sce}_results.csv', index_label='index', index=False)

    # Also save the results of all scenarios in the combined dataframe
   # results_df_combined_trucks.to_csv(r'../experiment\results_trucks\trucks_combined_results.csv', index=False)
    results_df_combined_bridges.to_csv(r'../experiment\results_bridges\bridges_combined_results.csv', index=False)

    end_time = datetime.now() # To keep track of run time

    print("The simulation started at ", start_time, "The end time of the simulation is ", end_time)
    print("Therefore the simulation ran for ",end_time-start_time)

if __name__ == "__main__":
    main()