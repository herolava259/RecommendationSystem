import tensorflow as tf

from tensorflow.keras.losses import Loss
from tensorflow.keras import backend as K


# pair-wise personalized ranking loss
class BayesianPersonalizedRankingLoss(Loss):
    def __init__(self, name: str = "bayesian-personalize-ranking-loss", **kwargs):
        super().__init__(name)

    def call(self, positive_samples, negative_samples):

        distances = positive_samples - negative_samples

        loss = tf.reduce_sum(tf.math.log(tf.sigmoid(distances)), axis=0, keepdims=True)
        return loss


