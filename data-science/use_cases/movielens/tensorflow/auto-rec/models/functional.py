import tensorflow as tf
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.initializers import RandomNormal, Zeros
from tensorflow.keras import backend as K
from tensorflow.keras.metrics import RootMeanSquaredError

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard, EarlyStopping
from tensorflow.keras import Input, Sequential, Model
from tensorflow.keras.layers import Embedding, StringLookup, Flatten, Lambda, Dense, Dropout
from tensorflow.keras.regularizers import L2
from tensorflow.data import Dataset as tf_dataset
from tensorflow.keras.activations import relu

def functional_api(input_dim, hidden_dim, dropout = 0.5, batch_size: int | None =None):
    input_layer = Input(shape = (input_dim,), batch_size = batch_size, dtype = tf.float32)

    encoder_layer = Dense(units = hidden_dim, activation = "sigmoid", use_bias = True,
                         kernel_initializer = RandomNormal(stddev = 0.01),
                         bias_initializer = Zeros(),
                         kernel_regularizer = L2())(input_layer)
    dropout_layer = Dropout(rate = dropout)(encoder_layer)
    decoder_layer = Dense(units = input_dim, activation = None, use_bias = True,
                         kernel_initializer = RandomNormal(stddev = 0.01),
                         bias_initializer = Zeros(),
                         kernel_regularizer = L2())(dropout_layer)

    model = Model(inputs = input_layer, outputs = decoder_layer)

    return model