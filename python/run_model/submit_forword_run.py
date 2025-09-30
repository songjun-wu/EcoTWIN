import os
import numpy as np
import time
import subprocess

from GEM_tools import checkTaskStatus



def submit_job(batch_ID, chain_start, chain_end):
    with open('batch_forward_run_copy.slurm', 'r') as f:
        lines = f.readlines()
        for xx, line in enumerate(lines):
            if '#SBATCH --job-name' in line:
                lines[xx] = '#SBATCH --job-name="EU'+str(batch_ID)+'"'
            elif 'srun --exclusive --cpu-bind=cores' in line:
                lines[xx] = 'srun --exclusive --cpu-bind=cores python3 forward_run.py --batch_ID ' + str(batch_ID) + ' --chain_start ' + str(chain_start) + ' --chain_end ' + str(chain_end)
    with open('batch_forward_run.slurm', 'w') as f:
        f.writelines(lines)
        
    subprocess.run(["sbatch", "batch_forward_run.slurm"],
               stdout=subprocess.DEVNULL,
               stderr=subprocess.DEVNULL,
               check=True)
    print('Submit job for batch ' + str(batch_ID) +'     chain : ' + str(chain_start) + '-' + str(chain_end), flush=True)
    time.sleep(5)


def is_job_done(batch_ID):

    if checkTaskStatus('EU'+str(batch_ID)) == 0:
        return True
    else:
        return False



if __name__ == "__main__":

    batch_ID_list = [2,3,4,5,6,7,8,9]



    chain_start_list = np.arange(0,40,2)
    chain_end_list = np.arange(0,40,2) + 2
    n_runs = len(chain_start_list)

    for i in range(n_runs):
        print(chain_start_list[i], chain_end_list[i])


    completed_runs = {i: 0 for i in batch_ID_list}


    for batch_ID in batch_ID_list:
        if is_job_done(batch_ID):
            chain_start = chain_start_list[completed_runs[batch_ID]]
            chain_end = chain_end_list[completed_runs[batch_ID]]
            submit_job(batch_ID, chain_start, chain_end)



    while True:
        time.sleep(10)  # Check every 10 s
        for batch_ID in batch_ID_list:
            if completed_runs[batch_ID] < n_runs and is_job_done(batch_ID):
                completed_runs[batch_ID] += 1
                print(f"Job {batch_ID} finished run {completed_runs[batch_ID]}/{n_runs}")

                # Continue to submit if maximum number of runs is not reached
                if completed_runs[batch_ID] < n_runs:
                    chain_start = chain_start_list[completed_runs[batch_ID]]
                    chain_end = chain_end_list[completed_runs[batch_ID]]
                    submit_job(batch_ID, chain_start, chain_end)

        # Break if all runs are completed
        if all(count == n_runs for count in completed_runs.values()):
            print("All jobs finished "+str(n_runs)+" times. Exiting.")
            break         


