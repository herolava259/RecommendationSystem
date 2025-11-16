import tensorflow as tf
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras import backend as K


class CustomMeanSquaredErrorLoss(tf.keras.losses.Loss):
    def __init__(self, name="mean_squared_loss"):
        super().__init__(name=name)
    def call(self, y_true, y_pred):
        error = y_true - y_pred
        squared_error = K.square(error)

        n = tf.shape(y_true)[0]
        loss = squared_error / n

        return loss
