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

for sce in range(1,3): #eight different scenarios
    for rep in range(1,3): #ten replications per scenario
        scenario = sce
        seed = random.seed()
        sim_model = BangladeshModel(seed=seed,scenario=scenario,replication=rep,run_length_model=run_length)
        for i in range(run_length):
            #print(i)
            sim_model.step()
            if i == run_length - 1:
                sim_model.save_results()

# Check if the seed is set
#print("SEED " + str(sim_model._seed))

# One run with given steps
#for i in range(run_length):
    #sim_model.step()
