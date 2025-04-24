# -*- coding: utf-8 -*-

import os
import shutil
import numpy as np
from mpi4py import MPI
from . import Dream_shared_vars
from .Dream import Dream
from .model import Model
import time
import traceback

def run_dream(parameters, likelihood, nchains=5, niterations=50000, start=None, restart=False, verbose=True, nverbose=10, tempering=False, **kwargs):
    """Run DREAM given a set of parameters with priors and a likelihood function."""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < nchains:
        if rank == 0:
            print(f"Warning: Number of MPI processes ({size}) is less than requested chains ({nchains}). Adjusting nchains to {size}.")
        nchains = size

    if restart:
        if start is None:
            raise Exception('Restart run specified but no start positions given.')
        if 'model_name' not in kwargs:
            raise Exception('Restart run specified but no model name to load history and crossover value files from given.')

    if type(parameters) is not list:
        parameters = [parameters]

    model = Model(likelihood=likelihood, sampled_parameters=parameters)

    if restart:
        step_instance = Dream(model=model, variables=parameters,
                              history_file=kwargs['model_name'] + '_DREAM_chain_history.npy',
                              crossover_file=kwargs['model_name'] + '_DREAM_chain_adapted_crossoverprob.npy',
                              gamma_file=kwargs['model_name'] + '_DREAM_chain_adapted_gammalevelprob.npy',
                              verbose=verbose, **kwargs)
        
    else:
        step_instance = Dream(model=model, variables=parameters, verbose=verbose, **kwargs)
        

    shared_vars = None
    if rank==0:
        
        shared_vars = _setup_mp_dream_pool(nchains, niterations, step_instance, start_pt=start)
        # Set Dream_shared_vars

        Dream_shared_vars.history = shared_vars['history']
        Dream_shared_vars.nseedchains = shared_vars['nseedchains']
        Dream_shared_vars.history_arr_shape = shared_vars['history'].shape
        Dream_shared_vars.current_positions = shared_vars['current_positions']
        Dream_shared_vars.nchains = 0
        Dream_shared_vars.cross_probs = shared_vars['cross_probs']
        Dream_shared_vars.ncr_updates = shared_vars['ncr_updates']
        Dream_shared_vars.delta_m = shared_vars['delta_m']
        Dream_shared_vars.gamma_level_probs = shared_vars['gamma_level_probs']
        Dream_shared_vars.ngamma_updates = shared_vars['ngamma_updates']
        Dream_shared_vars.delta_m_gamma = shared_vars['delta_m_gamma']
        Dream_shared_vars.count = shared_vars['count']
        Dream_shared_vars.history_seeded = shared_vars['history_seeded']

    Dream_shared_vars.win_history = None
    Dream_shared_vars.history = comm.bcast(Dream_shared_vars.history, root=0)
    Dream_shared_vars.nseedchains = comm.bcast(Dream_shared_vars.nseedchains, root=0)
    Dream_shared_vars.history_arr_shape = comm.bcast(Dream_shared_vars.history_arr_shape, root=0)
    Dream_shared_vars.current_positions = comm.bcast(Dream_shared_vars.current_positions, root=0)
    Dream_shared_vars.nchains = comm.bcast(Dream_shared_vars.nchains, root=0)
    Dream_shared_vars.cross_probs = comm.bcast(Dream_shared_vars.cross_probs, root=0)
    Dream_shared_vars.ncr_updates = comm.bcast(Dream_shared_vars.ncr_updates, root=0)
    Dream_shared_vars.delta_m = comm.bcast(Dream_shared_vars.delta_m, root=0)
    Dream_shared_vars.gamma_level_probs = comm.bcast(Dream_shared_vars.gamma_level_probs, root=0)
    Dream_shared_vars.ngamma_updates = comm.bcast(Dream_shared_vars.ngamma_updates, root=0)
    Dream_shared_vars.delta_m_gamma = comm.bcast(Dream_shared_vars.delta_m_gamma, root=0)
    Dream_shared_vars.count = comm.bcast(Dream_shared_vars.count, root=0)
    Dream_shared_vars.history_seeded = comm.bcast(Dream_shared_vars.history_seeded, root=0)
    

    # Create share memory for history
    _update_mp_dream_pool(Dream_shared_vars.nseedchains, niterations, step_instance, start_pt=start)




    try:
        if tempering:
            if rank == 0:
                sampled_params, log_ps = _sample_dream_pt(nchains, niterations, step_instance, start, verbose=verbose)
            else:
                _sample_dream_pt_chain((step_instance, start, None, None, None))  # Run
            comm.Barrier()
        else:
            if type(start) is list:
                start_point = start[rank] if rank < len(start) else None
            else:
                start_point = start

            if rank == 0 and not restart:
                if os.path.exists(kwargs['savePath']):
                    shutil.rmtree(kwargs['savePath'])
                os.makedirs(kwargs['savePath'])

            args = (step_instance, niterations, start_point, verbose, nverbose, rank,
                    kwargs.get('savePath', '.'), kwargs.get('total_iterations', niterations),
                    kwargs.get('model_name', 'dream'))

            _sample_dream(args)

    except:
        pass

def _sample_dream(args):
    try:
        dream_instance = args[0]
        iterations = args[1]
        start = args[2]
        verbose = args[3]
        nverbose = args[4]
        chainID = args[5]
        savePath = args[6]
        total_iterations = args[7]
        model_name = args[8]

        step_fxn = getattr(dream_instance, 'astep')
        q0 = start
        
        for iteration in range(iterations):
            old_params = q0

            sampled_params, log_prior, log_like = step_fxn(q0, chainID, total_iterations)

            log_ps = log_like + log_prior
            q0 = sampled_params

            if old_params is None:
                old_params = q0

            if iteration == 0:
                f_param = open(savePath + model_name + '_sampled_params_chain_' + str(chainID) + '_' + str(total_iterations) + '.bin', 'ab+')
                f_logps = open(savePath + model_name + '_logps_chain_' + str(chainID) + '_' + str(total_iterations) + '.bin', 'ab+')
            
            sampled_params.tofile(f_param)
            log_ps.tofile(f_logps)

            if chainID == 0:
                print(iteration, log_ps, flush=True)

        f_param.close()
        f_logps.close()

    except Exception as e:
        traceback.print_exc()
        print()
        raise e

def _setup_mp_dream_pool(nchains, niterations, step_instance, start_pt=None):
    min_njobs = (2 * len(step_instance.DEpairs)) + 1
    if nchains < min_njobs:
        raise Exception('Dream should be run with at least (2*DEpairs)+1 number of chains.  For current algorithmic settings, set njobs>=%s.' % str(min_njobs))
    
    if step_instance.history_file != False:
        old_history = np.load(step_instance.history_file)
        print('Precentage of nan value in history file  :  ', 1 - np.sum(~np.isnan(old_history)/len(old_history)), np.sum(~np.isnan(old_history)), len(old_history), flush=True)  # todo
        len_old_history = len(old_history.flatten())
        nold_history_records = len_old_history / step_instance.total_var_dimension
        step_instance.nseedchains = min(nold_history_records, step_instance.nseedchains)

        if niterations < step_instance.history_thin:
            arr_dim = ((np.floor(nchains * niterations / step_instance.history_thin) + nchains) * step_instance.total_var_dimension) + (step_instance.nseedchains * step_instance.total_var_dimension)
        else:
            arr_dim = np.floor((((nchains * niterations) * step_instance.total_var_dimension) / step_instance.history_thin)) + (step_instance.nseedchains * step_instance.total_var_dimension)
    else:
        if niterations < step_instance.history_thin:
            arr_dim = ((np.floor(nchains * niterations / step_instance.history_thin) + nchains) * step_instance.total_var_dimension) + (step_instance.nseedchains * step_instance.total_var_dimension)
        else:
            arr_dim = np.floor(((nchains * niterations / step_instance.history_thin) * step_instance.total_var_dimension)) + (step_instance.nseedchains * step_instance.total_var_dimension)

    min_nseedchains = 2 * len(step_instance.DEpairs) * nchains
    if step_instance.nseedchains < min_nseedchains:
        raise Exception('The size of the seeded ('+str(step_instance.nseedchains)+') starting history is insufficient.  Increase nseedchains>=%s.' % str(min_nseedchains))
    
    current_position_dim = nchains * step_instance.total_var_dimension


    # Start with nan values
    history_arr = np.full(int(arr_dim), np.nan)
    if step_instance.history_file != False:
        history_arr[0:step_instance.nseedchains * step_instance.total_var_dimension] = old_history[-(step_instance.nseedchains * step_instance.total_var_dimension):]
    nCR = step_instance.nCR
    ngamma = step_instance.ngamma
    crossover_setting = step_instance.CR_probabilities
    crossover_probabilities = np.array(crossover_setting)
    ncrossover_updates = np.zeros(nCR)
    delta_m = np.zeros(nCR)
    gamma_level_setting = step_instance.gamma_probabilities
    gamma_probabilities = np.array(gamma_level_setting)
    ngamma_updates = np.zeros(ngamma)
    delta_m_gamma = np.zeros(ngamma)
    current_position_arr = np.zeros(current_position_dim)
    shared_nchains = nchains
    n = 0
    tf = b'F'
    
    return {
        'history': history_arr,
        'current_positions': current_position_arr,
        'nchains': shared_nchains,
        'nseedchains': step_instance.nseedchains,
        'cross_probs': crossover_probabilities,
        'ncr_updates': ncrossover_updates,
        'delta_m': delta_m,
        'gamma_level_probs': gamma_probabilities,
        'ngamma_updates': ngamma_updates,
        'delta_m_gamma': delta_m_gamma,
        'count': n,
        'history_seeded': tf
    }


def _update_mp_dream_pool(nseedchains, niterations, step_instance, start_pt=None):

    step_instance.niterations = niterations

    step_instance.nseedchains = nseedchains

    if step_instance.crossover_burnin is None:
        step_instance.crossover_burnin = int(np.floor(step_instance.niterations / 10))

    if start_pt is not None and step_instance.start_random:
        print('Warning: start position provided but random_start set to True. Overrode random_start value and starting walk at provided start position.')
        step_instance.start_random = False