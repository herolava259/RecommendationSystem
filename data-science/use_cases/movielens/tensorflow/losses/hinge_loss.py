import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.losses import Loss


class CustomHingeLoss(Loss):
    def __init__(self, margin: float):
        super().__init__()
        self.margin = margin

    def call(self, y_positive: tf.Tensor, y_negative: tf.Tensor) -> tf.Tensor:

        distances = y_positive - y_negative

        loss = tf.reduce_sum(tf.math.maximum(-distances+ self.margin, 0))

        return loss

