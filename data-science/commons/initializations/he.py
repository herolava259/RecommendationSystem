from .random import uniform_random, normal_random
import numpy as np

def he_with_normal(fan_in, fan_out):
    sigma_square = 2 / fan_in

    return normal_random(fan_in, fan_out, scale=np.sqrt(sigma_square), loc=0.0)

def he_with_uniform(fan_in, fan_out):

    r = np.sqrt(6 / fan_in)

    return uniform_random(fan_in, fan_out) * r 


