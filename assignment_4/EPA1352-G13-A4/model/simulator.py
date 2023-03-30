import multiprocessing as mp
import pandas as pd
from model import BangladeshModel

def perform_experiment(core_number,job):
    # Initiate model.
    sce = job[0][0]
    rep = job[0][1]

    dict = job[1]
    shortest_routes_sourcesinks = dict['shortest_routes_sourcesinks']
    seed = dict['seed']
    file = dict['file']
    run_length = dict['run_length']

    sim_model = BangladeshModel(shortest_routes_sourcesinks, seed=seed,file = file,scenario=sce,replication=rep)
    for i in range(run_length):  # Run model as long as the run_length.
        if i % 100 == 0:
            print(f'CORE {core_number}: At step {i} for replication {rep} for scenario {sce}')
        sim_model.step()
    print(f'CORE {core_number}: Finished replication {rep} for scenario {sce}')
    results_df = sim_model.save_results()
    return results_df

def proc_func(procnum, jobs_r, results_w):
    running = True
    while running:
        job = jobs_r.recv()
        if job is None:
            results_w.send(None)
            running = False
        else:
            result = perform_experiment(procnum, job)
            results_w.send(result)

def perform_multi_threading(sce_rep_dict): # confirms that the code is under main function
    # instantiating process with arguments
    combined = pd.DataFrame()
    procs = []
    results = []
    num_procs = max(1, mp.cpu_count()-2) # Start at least 1 process
    # Setup processes and pipes
    for procnum in range(num_procs):
        jobs_r, jobs_w = mp.Pipe(False)
        results_r, results_w = mp.Pipe(False)
        proc = mp.Process(target=proc_func, args=(procnum, jobs_r, results_w), name=f"Process-{procnum}")
        proc.start()
        procs.append((procnum, proc, jobs_w, results_r))

    # Submit jobs, reading results if available
    for i, job in enumerate(sce_rep_dict.items()):
        core = procs[i%num_procs]
        procnum, proc, jobs_w, results_r = core
        jobs_w.send(job)

    # Send termination signals, reading results if available
    for procnum, _, jobs_w, results_r in procs:
        jobs_w.send(None)
        jobs_w.close()

    # Read final results
    unfinished = procs[:] # Clone procs
    while unfinished:
        for i in range(len(unfinished)):
            procnum, _, _, results_r = unfinished[i]
            if results_r.poll():
                result = results_r.recv()
                if result is None:
                    results_r.close()
                    del unfinished[i]
                    #print(f"Process {procnum} is done")
                    break # We've invalidated i, so break out to the outer while
                else:
                    df = result
                    combined = pd.concat([combined, df])

    # Clean up
    for procnum, proc, _, _ in procs:
        proc.join()
        #print(f"Joined process {procnum}")

    return combined

def perform_single_threading(sce_rep_dict):
    combined = pd.DataFrame()
    for job in sce_rep_dict.items():
        df = perform_experiment(0,job)
        combined = pd.concat([combined,df])

    return combined