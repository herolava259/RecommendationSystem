import numpy as np

def factor(fan_in, fn_out):
    return np.sqrt(1/ fan_in)