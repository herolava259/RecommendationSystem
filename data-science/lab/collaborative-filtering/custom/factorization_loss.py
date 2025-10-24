import numpy as np


def factorization_loss(x_data: np.ndarray, x: np.ndarray, w: np.ndarray, rating_mask: np.ndarray, _lambda: float) -> float:
    num_ratings = np.sum(rating_mask)

    ui_pairs = np.where(rating_mask == 1)

    loss = 0.0

    for u, i in ui_pairs:
        loss += (x_data[i, u] - x[i,:] @ w[u, :]) ** 2

    loss /= num_ratings

    loss += _lambda * np.sum(x ** 2 + w **2)

    loss /= 2

    return loss


