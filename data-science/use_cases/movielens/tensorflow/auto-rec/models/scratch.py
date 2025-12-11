from tensorflow import Module
from tensorflow.keras.utils import Sequence
from tensorflow.keras.layers import Activation
from tensorflow.keras.activations import relu
import tensorflow as tf
import numpy as np
from tensorflow.keras.initializers import HeUniform
from typing import List, Dict, Any

class FinegrainedRecModel(Module):
    def __init__(self, hidden_dim: int, input_dim: int, dropout: float = 0.5, seed: int = 42, _lambda: float = 0.89):
        super().__init__()
        self.hidden_dim: int = hidden_dim
        self.input_dim: int = input_dim

        # declare encoder
        # hidden layer: shape = input_dim * hidden_dim (weights) + hidden_dim (bias)
        initializer = HeUniform()
        self.encoder_weight = tf.Variable(initial_value=initializer(shape=(hidden_dim, input_dim)), dtype=tf.float32)

        self.decoder_weight = tf.Variable(initial_value=initializer(shape=(input_dim, hidden_dim)), dtype=tf.float32)

        self.encoder_bias = tf.Variable(initial_value=tf.zeros(shape=(hidden_dim,)), dtype=tf.float32)

        self.decoder_bias = tf.Variable(initial_value=tf.zeros(shape=(input_dim,)), dtype=tf.float32)

        self._lambda = _lambda

        self.dropout = dropout
        self.seed = seed

    def _dropout_msk(self, batch_size: int = 1):
        size = self.hidden_dim
        weight_probs = tf.random.uniform(shape=[batch_size, size])

        return tf.squeeze(tf.cast(weight_probs < self.dropout, dtype=tf.float32))

    def forward(self, inputs: tf.Tensor| np.ndarray, training: bool = False) -> tf.Tensor:
        if isinstance(inputs, np.ndarray):
            inputs = tf.constant(inputs, dtype=tf.float32)

            # encoder forward : linear compute -> activation with sigmoid -> dropout
        enc_ws = self.encoder_weight
        enc_bias = self.encoder_bias

        dec_ws = self.decoder_weight
        dec_bias = self.decoder_bias

        batch_forward = False
        batch_shape = 1

        if tf.shape(tf.shape(inputs)) == 2:
            batch_forward = True
            batch_shape = tf.shape(inputs)[0].numpy()
            enc_ws = tf.tile(tf.expand_dims(enc_ws, axis=0), multiplies=tf.constant([batch_shape, 1, 1], tf.int32))
            enc_bias = tf.tile(tf.expand_dims(enc_bias, axis=0), multiplies=tf.constant([batch_shape, 1], tf.int32))

            dec_ws = tf.tile(tf.expand_dims(dec_ws, axis=0), multiples=tf.constant([batch_shape, 1, 1], tf.int32))
            dec_bias = tf.tile(tf.expand_dims(dec_bias, axis=0), multiples=tf.constant([batch_shape, 1], tf.int32))

        # compute linear f(x) = W @ inputs + bias . @ meaning dot product of two vector or matrix

        # case: batch : shape(inputs) = batch_size x input_dim. shape(enc_ws now) = batch_size x hidden_dim x xinput_dim. shape(enc_bias) = batch_size x hidden_dim
        x = inputs * enc_ws

        x = tf.reduce_sum(x, axis=-1) + enc_bias

        # activation: sigmoid f(x) = 1 / 1 + e**-x

        x = 1 / (1 + tf.math.exp(-x))

        if training:
            # drop some neuron in hidden layers
            dropout_msk = self._dropout_msk(batch_shape)
            x = dropout_msk * x

        y = tf.reduce_sum(x * dec_ws, axis=-1) + dec_bias

        return y

    def compute_loss(self, y_pred, y_true, has_l2: bool = False):
        assert tf.shape(tf.shape(y_pred)) == tf.shape(tf.shape(y_true))

        loss = tf.reduce_mean((y_pred - y_true) ** 2)

        if has_l2:
            loss += self._lambda * tf.reduce_sum(self.encoder_weight ** 2 + self.decoder_weight ** 2)

        return loss

    def rmse_eval(self, y_true, y_pred):
        return tf.sqrt(tf.reduce_mean((y_pred - y_true) ** 2))

    def predict(self, x_test):
        return self.forward(x_test, training=False)
    def evaluate(self, x_val, y_val):
        y_pred = self.predict(x_val)
        return self.rmse_eval(y_val, y_pred)

    def fit(self, x_train, y_train, x_val, y_val, batch_size: int = 32, num_epochs=4, rnd_seed: int =42):
        # validate type : should be tf.Tensor, np.array
        tf.random.set_seed(rnd_seed)

        history: Dict[str, List[Any]] = {"loss": [], "train-error": [], "eval-error": []}

        losses = tf.TensorArray(dtype=tf.float32, size=num_epochs)
        training_scores = tf.TensorArray(dtype=tf.float32, size=num_epochs)
        eval_scores = tf.TensorArray(dtype=tf.float32, size=num_epochs)

        train_size = tf.shape(x_train)[0].numpy()
        eval_size = tf.shape(x_val)[0].numpy()

        shuffle_size = min(batch_size << 4, train_size // 4)

        shuffle_size = max(shuffle_size // batch_size, 1) * batch_size

        # create a optimizer, preference Adagrad
        optimizer = tf.keras.optimizers.Adagrad(
            learning_rate=0.002,
            weight_decay=1e-5)
        num_steps = train_size // batch_size + int(train_size % batch_size == 0)
        for i in range(num_epochs):

            epoch_losses = tf.TensorArray(dtype=tf.float32, size=num_steps)
            epoch_errors = tf.TensorArray(dtype=tf.float32, size=num_steps)

            # train step
            step = 0
            p_buff = 0
            p_start = 0
            p_end = shuffle_size

            buffer_ids = None

            for batch_idx in range(0, train_size, batch_idx):

                # data preparation
                if batch_idx % shuffle_size == 0:
                    p_start = batch_idx
                    p_end = min(p_start + shuffle_size, train_size)
                    buffer_ids = tf.random.shuffle(tf.range(p_start, p_end, dtype=tf.int32))
                    p_buff = 0

                batch_train_ids = buffer_ids[p_buff: min(p_buff + batch_size, shuffle_size)]

                x_batch = tf.gather(x_train, indices=batch_train_ids, axis=0)
                y_batch = tf.gather(x_train, indices=batch_train_ids, axis=0)

                with tf.GradientTape(persistent=True) as tape:
                    tape.watch(self.encoder_weight)
                    tape.watch(self.decoder_weight)
                    tape.watch(self.encoder_bias)
                    tape.watch(self.decoder_bias)

                    y_pred = self.forward(x_batch, training=True)

                    loss = self.compute_loss(y_pred, y_batch, has_l2=True)

                    epoch_losses.write(num_steps, loss)

                epoch_errors.write(num_steps, self.rmse_eval(y_batch, y_pred))

                # compute gradient, evaluate on training data set save to eval-training dataset
                enc_w_grad = tape.gradient(loss, self.encoder_weight)
                enc_b_grad = tape.gradient(loss, self.encoder_bias)

                dec_w_grad = tape.gradient(loss, self.decoder_weight)
                dec_b_grad = tape.gradient(loss, self.decoder_bias)

                # print loss, error during training, or print eval error

                step = (step + 1) % num_steps

                if step % 20 == 0:
                    print(f"Avg Loss on training: {tf.reduce_mean(epoch_losses.concat()).numpy()}")
                    print(f"Avg error on training data: {tf.reduce_mean(epoch_errors.concat()).numpy()}")

            # evaluate the model on the eval dataset
            print(f"End of epoch {i} \n Summary: ")
            eval_errors = tf.concat([self.evaluate(
                x_val[batch_idx: min(batch_idx + batch_size, eval_size)],\
                y_val[batch_idx: min(batch_idx + batch_size, eval_size)]) \
                for batch_idx in range(0, eval_size, batch_size)], axis=0)

            avg_epoch_error = tf.reduce_mean(eval_errors)
            print(f"Avg loss on training data: MSE= {tf.reduce_mean(epoch_losses.concat()).numpy()}")
            print(f"Avg error on training data: RMSE= {tf.reduce_mean(epoch_errors.concat()).numpy()}")
            print(f"Avg error on training data: RMSE= {avg_epoch_error.numpy()}")

            losses.write(i, tf.reduce_mean(epoch_losses.concat()))
            training_scores.write(i, tf.reduce_mean(epoch_errors.concat()))
            eval_scores.write(i, avg_epoch_error)

        return {"training_losses": losses.stack(), "training_accuracy": training_scores.stack(),
                "eval_accuracy": eval_scores.stack()}

