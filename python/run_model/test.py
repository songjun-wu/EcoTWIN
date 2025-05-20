from mpi4py import MPI
import numpy as np

# Simulated model evaluation function
def evaluate_model(model_id, params):
    np.random.seed(model_id + int(np.sum(params) * 1000))
    return -((params[model_id % len(params)] - model_id) ** 2) + np.random.normal(0, 0.1)

def propose_new_params(current_params, global_history, iteration, chain_idx):
    # Simple random walk proposal (replace with DREAM's differential evolution)
    return current_params + np.random.normal(0, 0.1, size=current_params.shape)

def metropolis_accept(loglike_new, loglike_old):
    if loglike_old is None or loglike_new > loglike_old:
        return True
    return np.random.rand() < np.exp(loglike_new - loglike_old)

# MPI init
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
assert size == 6, "This script requires exactly 50 MPI processes."

# Chain layout
chain_id = rank // 2
model_id = rank % 2

# Intra-chain communicator (5 ranks per chain)
subcomm = comm.Split(color=chain_id, key=rank)
subrank = subcomm.Get_rank()

# Inter-chain communicator (only chain masters)
is_chain_master = model_id == 0
master_comm = comm.Split(color=0 if is_chain_master else MPI.UNDEFINED, key=rank)

# Shared history parameters
n_chains = 3
param_dim = 3
max_iter = 2

if is_chain_master:
    master_rank = master_comm.Get_rank()
    # Allocate full shared history array on rank 0 of master_comm
    if master_rank == 0:
        history = np.zeros((max_iter, n_chains, param_dim), dtype='d')
    else:
        history = None
    win = MPI.Win.Create(history, comm=master_comm)
else:
    win = None
    history = None

# Initial state
params = np.random.rand(param_dim)
loglike_old = None
chain_history = []

# Run MCMC
for iteration in range(max_iter):
    if is_chain_master:
        master_rank = master_comm.Get_rank()

        # Chain master fetches full history if needed
        global_history = np.empty((max_iter, n_chains, param_dim), dtype='d')
        win.Fence()
        win.Get(global_history, target_rank=0)
        win.Fence()

        # Propose new parameters based on local history
        new_params = propose_new_params(params, global_history, iteration, master_rank)
    else:
        new_params = None

    # Broadcast proposed params to all model ranks in this chain
    new_params = subcomm.bcast(new_params, root=0)

    # Each rank evaluates one model
    local_like = evaluate_model(model_id, new_params)

    # Gather local likelihoods to chain master
    all_likes = subcomm.gather(local_like, root=0)

    if is_chain_master:
        avg_like = np.mean(all_likes)

        # Accept/reject step
        if metropolis_accept(avg_like, loglike_old):
            params = new_params
            loglike_old = avg_like

        # Save to local history
        chain_history.append((params.copy(), loglike_old))

        # Update global shared history (only master_rank == 0 actually stores)
        if master_rank == 0:
            offset = iteration * n_chains + master_rank
            history[iteration, master_rank, :] = params

# Save chain trace to file (only chain masters)
if is_chain_master:
    import pickle
    with open(f"chain_{chain_id}.pkl", "wb") as f:
        pickle.dump(chain_history, f)
