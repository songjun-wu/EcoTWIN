from pydream.core import run_dream
from pydream.parameters import SampledParam
from scipy.stats import norm
import numpy as np

def likelihood(params, chainID):
    return -0.5 * np.sum(params ** 2)  # Example Gaussian likelihood

parameters = [SampledParam(norm, loc=0, scale=1)]
sampled_params, log_ps = run_dream(
    parameters,
    likelihood,
    niterations=1000,
    verbose=True,
    savePath='./output/',
    model_name='test'
)
if sampled_params is not None:
    print(f"Sampled parameters shape: {[p.shape for p in sampled_params]}")