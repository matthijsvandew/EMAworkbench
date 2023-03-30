from model import BangladeshModel
from road_graph_nx import road_graph
import pandas as pd
import random
from datetime import datetime

import simulator

def main():
    start_time = datetime.now()

    print("The start time of the simulation =", start_time)

    """
        Run simulation
        Print output at terminal
    """

    # ---------------------------------------------------------------
    run_settings_dict = {}

    # The long run length reflects the run that will be used for experimentation.
    # run time 5 x 24 hours x 60 minutes; 1 tick 1 minute.
    long_run_length = 5 * 24 * 60

    # The short run length reflects a run that will be used for debugging because it is a lot faster.
    short_run_length = 500

    debug_run = False # If we want to debug: use the shorter run length.
    if debug_run == True:
        run_settings_dict['run_length'] = short_run_length
    else:
        run_settings_dict['run_length'] = long_run_length

    run_settings_dict['seed'] = True

    multiprocessing = True

    file = '../data\input_data.csv'
    run_settings_dict['file'] = file

    run_settings_dict['shortest_routes_sourcesinks'] = road_graph.find_shortest_path(file_name=file) # Find the shortest paths from every node to every other node in the network.
                                                                                # Call the find_shortest_path in the road_graph class, which are in the road_graph_nx.py file.

    sce_rep_dict = {}

    for sce in range(5): # Five different scenarios.
        # Initiate an empty dataframe. We will store all data for a single scenario over all replications there.
        for rep in range(1,11): # Ten replications per scenario.
            sce_rep_dict[(sce, rep)] = run_settings_dict

    if multiprocessing == True:
        results_df_combined = simulator.perform_multi_threading(sce_rep_dict)
    else:
        results_df_combined = simulator.perform_single_threading(sce_rep_dict)

    scenarios = results_df_combined['scenario'].unique()
    for i in scenarios:
        if i == 0:
            results_df_combined.loc[results_df_combined['scenario'] == 0].to_csv\
                (r'../experiment\base_case_results.csv', index_label='index')
        else:
            results_df_combined.loc[results_df_combined['scenario'] == i].to_csv \
                (f'../experiment\scenario{sce}_results.csv', index_label='index')

    results_df_combined.to_csv('../experiment\combined_results.csv')

    end_time = datetime.now()

    print("The simulation started at ", start_time, "The end time of the simulation is ", end_time)
    print("Therefore the simulation ran for ",end_time-start_time)

if __name__ == "__main__":
    main()