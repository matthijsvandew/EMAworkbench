from model import BangladeshModel
from try_nx import road_network

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
run_length = 5 * 24 * 60

# run time 1000 ticks
# run_length = 1000

seed = 1234567

shortest_routes_sourcesinks = road_network.find_shortest_path()

sim_model = BangladeshModel(shortest_routes_sourcesinks,seed=seed)

# Check if the seed is set
print("SEED " + str(sim_model._seed))

# One run with given steps
for i in range(run_length):
    sim_model.step()
