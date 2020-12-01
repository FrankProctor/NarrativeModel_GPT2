from sklearn.utils.fixes import loguniform
from scipy.stats.distributions import uniform
from sklearn.model_selection import ParameterSampler
import numpy as np


TUNING_PARAMS = {
    'learning_rate': loguniform(5e-6, 5e-2),
    'weight_decay': uniform(scale=0.3),
    'adam_epsilon': loguniform(1e-10, 1e-2),
    'max_grad_norm': uniform(loc=0.9, scale=0.2),
    'num_train_epochs': [1, 2],
}

FIX_PARAMS = {
}


def enumerate_config(num_config, seed=0):
    rng = np.random.RandomState(seed)

    config = list(
        ParameterSampler(
            TUNING_PARAMS,
            n_iter=num_config,
            random_state=rng))

    return enumerate([{**x, **FIX_PARAMS} for x in config])
