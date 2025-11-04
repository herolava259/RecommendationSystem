import numpy as np


def hinge_loss(positive: np.ndarray, negative: np.ndarray, margin = 1) -> float:

    distance = positive - negative

    return np.sum(np.maximum(margin - distance, 0))
