from .random import uniform_random, normal_random

import numpy as np


def xavier_with_normal(fan_in: int, fan_out: int) -> np.ndarray:

    sigma_squared = 2 / (fan_in + fan_out)

    return normal_random(fan_in, fan_out, scale=np.sqrt(sigma_squared))

def xavier_with_uniform(fan_in: int, fan_out: int) -> np.ndarray:

    r = np.sqrt(3 / (fan_in + fan_out))

    return uniform_random(fan_in, fan_out, low = 0, high=1) * r



