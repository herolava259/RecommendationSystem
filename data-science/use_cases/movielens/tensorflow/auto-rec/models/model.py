from tensorflow.keras.layers import Activation, Dropout
from tensorflow_lattice.layers import Linear
from tensorflow.keras import Model
from tensorflow.keras.activations import relu
from tensorflow.keras.regularizers import L2

class AutoRecModel(Model):
    def __init__(self, input_shape: int, hidden_dim: int, dropout: float = 0.5, batch_size: int | None = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.encoder_linear = Linear(num_input_dims=input_shape,
                                     units=hidden_dim,
                                     use_bias=True,
                                     kernel_initializer="random_uniform",
                                     bias_initializer="zeros",
                                     kernel_regularizer=L2())
        self.encoder_activation = Activation(activation=relu)
        self.encoder_dropout = Dropout(rate=dropout)
        self.decoder_linear = Linear(num_input_dims=hidden_dim,
                                     units=input_shape,
                                     use_bias=True,
                                     kernel_initializer="random_uniform",
                                     bias_initializer="zeros",
                                     kernel_regularizer=L2())

        self.input_shape = input_shape
        self.hiddden_dim = hidden_dim
        self.batch_size = batch_size

    def call(self, X):
        # test whether with any layer can proceed data with batch_size

        forward_output = self.encoder_linear(X)
        forward_output = self.encoder_activation(forward_output)
        forward_output = self.encoder_dropout(forward_output)
        forward_output = self.decoder_linear(forward_output)

        return forward_output
