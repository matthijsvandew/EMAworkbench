import multiprocessing as mp
import pandas as pd

#Definiëren scenario's. Ik zal ze hier in een lijst zetten. In het echt gaat dat iets gecompliceerder
list_runs = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2]]

def perform_experiment(core_number,run):
    # hier zou dus iets moeten gebeuren met de input. In het echte model willen we een dataframe returnen
    # deze dataframe zou aan het einde van alle runs samengevoegd moeten worden.
    sce, rep = run
    #print(f'core: {core_number} performing scenario: {sce} replication: {rep}')
    dict_new_run = {'scenario':sce,'replication':rep,'core':core_number}
    dataframe = pd.DataFrame.from_dict([dict_new_run])
    return dataframe

def merge_experiment_dataframes(experimental_results):
    final_dataframe = pd.DataFrame()
    for i in experimental_results:
        pd.concat([final_dataframe,i])
    return final_dataframe

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

def perform_multi_threading(): # confirms that the code is under main function
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
    for i, job in enumerate(list_runs):
        core = procs[i%num_procs]
        procnum, proc, jobs_w, results_r = core
        while results_r.poll():
            text, df = results_r.recv()
            #print(f"From {procnum}: {text}")
            results.append(df)
        jobs_w.send(job)

    # Send termination signals, reading results if available
    for procnum, _, jobs_w, results_r in procs:
        while results_r.poll():
            text, df = results_r.recv()
            #print(f"From {procnum}: {text}")
            results.append(df)
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
                    print(df)
                    combined = pd.concat([combined, df])
                    print(combined)

    # Clean up
    for procnum, proc, _, _ in procs:
        proc.join()
        #print(f"Joined process {procnum}")

def perform_single_threading():
    combined = pd.DataFrame()
    results = []
    for job in list_runs:
        df = perform_experiment(0,job)
        print(df)
        combined = pd.concat([combined,df])

    print(combined)

if __name__ == "__main__":
    #perform_single_threading()
    perform_multi_threading()
