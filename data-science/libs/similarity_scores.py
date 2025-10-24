import numpy as np


def similarity_score(x_features: np.ndarray, y_features: np.ndarray) -> float:

    return float(np.dot(x_features.T, y_features))