import numpy as np


def normal_random(fan_in, fan_out,loc: float = 0.0, scale: float = 1.0):
    return np.random.normal(size=(fan_in, fan_out),loc = loc, scale=scale)


def uniform_random(fan_in, fan_out, low: float = 0.0, high: float = 1.0):
    return np.random.uniform(low, high, size=(fan_in, fan_out))

