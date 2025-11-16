from abc import ABC, abstractmethod
from typing import List, Set, Any, Tuple, overload

from tensorflow import Module, GradientTape
from tensorflow.keras.optimizers import Optimizer
from tensorflow.keras.initializers import RandomNormal, Zeros

import tensorflow as tf


class RecLayer(Module, ABC):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @abstractmethod
    def forward(self, inputs, training: bool = False) -> tf.Tensor | Any:
        pass

    @abstractmethod
    def backward_with_optimizer(self, tape: GradientTape, loss: tf.Tensor, optimizer: Optimizer | None = None):
        pass

    @abstractmethod
    def simple_backward(self, tape: GradientTape, loss: tf.Tensor, lr: float = 0.002):
        pass

    @abstractmethod
    def monitor_variables(self, tape: GradientTape):
        pass

    @abstractmethod
    def get_variables(self) -> Any:
        pass

    def call(self, inputs):
        return self.forward(inputs)

    @abstractmethod
    def initialize(self, **kwargs):
        pass


class RecLatentFeatureLayer(RecLayer):
    def __init__(self, vocab: List[str] | Set[str], embedding_dim: int, **kwargs):
        kwargs["trainable"] = True
        kwargs["dtype"] = tf.float
        super().__init__(RecLatentFeatureLayer, self).__init__(**kwargs)
        self.vocab = tf.constant(vocab, dtype=tf.string)
        self.embedding_dim = embedding_dim
        self.n_space = tf.shape(self.vocab)[0]
        self.name2ids = None
        self.embed_vars = None
        self.bias = None
        self.embed_oov = None
        self.bias_oov = None
        self.additional_args: dict = kwargs

    def initialize(self):
        ids = tf.range(start=0, limit=self.n_item, delta=1, name=f"{self.name}-range")

        self.name2ids = tf.lookup.StaticHashTable(initializer=tf.lookup.KeyValueTensorInitializer(self.vocab, ids),\
                                                  key_dtype=tf.string, value_dtype=tf.int32, default_value="OOV")

        w_init = RandomNormal(std=0.01)
        b_init = Zeros()

        self.embed_vars = [tf.Variable(w_init(shape=(self.embedding_dim, )), dtype=tf.float32, trainable=True)
                           for _ in range(self.n_space)]

        self.bias = [tf.Variable(b_init(shape=(None,), dtype=tf.float32, trainable=True) for i in range(self.n_space)]

        self.embed_oov = tf.constant(w_init(shape=(self.embedding_dim,)), dtype=tf.float32 )
        self.bias_oov = tf.constant(w_init(shape=(1,)), dtype=tf.float32)

    def _forward_batch_training(self, inputs: tf.Tensor):
        extr_ids = tf.sparse.to_dense(self.name2ids.lookup(inputs))
        # assert all identifiers in vocab
        # end assert
        extr_ids = tf.sparse.to_dense(self.name2ids.lookup(inputs))

        return tf.gather(self.embed_vars, extr_ids, axis=0), tf.gather(self.bias, extr_ids, axis=0)

    def _forward_batch_predict(self, inputs: tf.Tensor):
        # out of vocab index
        extr_ids = tf.sparse.to_dense(self.name2ids.lookup(inputs)).numpy()

        # rerieve ids of ids in vocabulary

        length = tf.shape[0]

        embed_result = []
        bias_result = []

        for idx in extr_ids:
            if idx == -1:
                embed_result.append(self.embed_oov)
                bias_result.append(self.bias_oov)
            else:
                embed_result.append(self.embed_vars[idx])
                bias_result.append(self.bias[idx])

        return embed_result, bias_result

    def _forward_single_training(self, inputs: tf.Tensor):
        extr_id = tf.sparse.to_dense(self.name2ids.lookup(inputs))

        return self.embed_vars[extr_id], self.bias[extr_id]

    def _forward_single_predict(self, inputs: tf.Tensor):
        extr_id = tf.sparse.to_dense(self.name2ids.lookup(inputs))

        if tf.reduce_any(tf.equal(inputs, tf.constant(-1, dtype=tf.int32))).numpy():
            return self.embed_oov, self.bias_oov
        return self.embed_vars[extr_id], self.embed_bias[extr_id]

    def forward(self, inputs, training: bool = False):

        # validate inputs

        # convert to tf.Tensor if need

        # extract embedding vactors and bias

        batch_forward = True

        input_shape = tf.shape(inputs)

        # validate volume dim and raise errors

        if input_shape[0] > 1:
            batch_forward = False

        if training:
            return self._forward_batch_training(inputs) if batch_forward else \
                self._forward_single_training(inputs)
        else:
            return self._forward_batch_predict(inputs) if batch_forward else \
                self._forward_single_training(inputs)

    def monitor_variables(self, tape: GradientTape):
        [tape.watch(var) for var in self.embed_vars]
        tape.watch(self.bias)

    def get_variable(self) -> Tuple[tf.Variable, tf.Variable]:
        return self.embed_vecs, self.bias

    def simple_backward(self, tape: GradientTape, loss: Any, batch_ids: tf.Tensor, lr: float = 0.002):

        batch_ids = set(self.lookup_ids(batch_ids).numpy())

        for i in batch_ids:
            embed_gradient = tape.gradient(loss, self.embed_vars[i])
            bias_gradient = tape.gradient(loss, self.bias[i])
            self.embed_vars[i].assign_sub(embed_gradient * lr)
            self.bias[i].assign_sub(bias_gradient * lr)

    def backward_with_optimizer(self, tape: GradientTape, loss: Any, batch_ids: tf.Tensor, optimizer: Optimizer):

        batch_ids = set(self.lookup_ids(batch_ids).numpy())

        for i in range(self.n_space):
            embed_gradient = tape.gradient(loss, self.embed_vars[i])
            bias_gradient = tape.gradient(loss, self.bias[i])
            optimizer.apply_gradients(zip(embed_gradient, self.embed_vars[i]))
            optimizer.apply_gradients(zip(embed_gradient, self.bias[i]))


class FineGrainedMFModel(Module):
    def __init__(self, user_vocab, item_vocab, embedding_dim, _lambda: bool = 0.25):

        self.u_vocab = user_vocab
        self.i_vocab = item_vocab
        self.embedding_dim = embedding_dim

        ## embedding vectors
        self.u_latent = RecLatentFeatureLayer(self.u_vocab, embedding_dim, name="user-latent-layer")
        self.i_latent = RecLatentFeatureLayer(self.i_vocab, embedding_dim, name="item-latent-layer")
        # lamda factor for l2 regularization
        self._lambda = _lambda

    @staticmethod
    def _retriever_tensor_score(self, u_vec: Tuple[tf.Tensor, tf.Tensor],
                                i_vec: Tuple[tf.Tensor, tf.Tensor],
                                training: bool = False) -> tf.Tensor:
        u_latent, u_bias = u_vec
        i_latent, i_bias = i_vec

        return tf.reduce_sum(tf.multiple(u_latent, i_latent), axis=-1) + u_bias + i_bias

    @staticmethod
    def _retriever_batch_score(self, u_vas: List[Tuple[tf.Tensor, tf.Tensor]] | Tuple[tf.Tensor, tf.Tensor],
                               i_vas: List[Tuple[tf.Tensor, tf.Tensor]] | Tuple[tf.Tensor, tf.Tensor]) -> tf.Tensor:

        if isinstance(u_vas, list):
            u_vecs = tf.convert_to_tensor([pair[0] for pair in u_vas], dtype=tf.float32)
            u_bias = tf.convert_to_tensor([pair[1] for pair in u_vas], dtype=tf.float32)

        else:
            u_latent, u_bias = u_vas

        if isinstance(i_vas, list):
            i_vecs = tf.convert_to_tensor([pair[0] for pair in i_vas], dtype=tf.float32)
            i_bias = tf.convert_to_tensor([pair[1] for pair in i_vas], dtype=tf.float32)
        else:
            i_vecs, i_bias = i_vas

        return tf.reduce_sum(tf.multiple(u_vecs, i_vecs), axis=-1) + u_bias + i_bias

    def forward(self,
                inputs: Tuple[tf.Tensor, tf.Tensor] | List[Tuple[tf.Tensor, tf.Tensor]] | List[tf.Tensor] | tf.Tensor, \
                training: bool = False) -> tf.Tensor:
        u_ids, i_ids = None, None

        if isinstance(inputs, tuple):
            u_ids, i_ids = inputs

        elif isinstance(inputs, list):
            if isinstance(inputs[0], tuple):
                u_ids = tf.convert_to_tensor([pair[0] for pair in inputs], dtype=tf.string)
                i_ids = tf.convert_to_tensor([pair[1] for pair in inputs], dtype=tf.string)
            elif isinstance(inputs[0], tf.Tensor):
                inputs = tf.constant(inputs, dtype=tf.string)
                u_ids = inputs[:, 0]
                i_ids = inputs[:, 1]
            else:
                raise TypeError("Invalid type of inputs")
        elif isinstance(inputs, tf.Tensor):
            if len(tf.shape(inputs)) == 1 and (tf.shape(inputs)[0] == 2):
                u_ids = inputs[0]
                i_ids = inputs[1]
            elif len(tf.shape(inputs)) == 2 and (tf.shape(inputs)[1] == 2):
                u_ids = inputs[:, 0]
                i_ids = inputs[:, 1]
            else:
                raise TypeError("Invalid type of argument inputs")
        else:
            raise TypeError("Invalid type of argument inputs")

        u_vecs, u_biases = self.u_latent.forward(u_ids, training=training)
        i_vecs, i_biases = self.i_latent.forward(i_ids, training=training)

        return FineGrainedMFModel.\
            _retriever_batch_score(
                u_vas=(tf.convert_to_tensor(u_vecs, dtype=tf.float32), tf.convert_to_tensor(u_biases, dtype=tf.float32)),
                i_vas=(tf.convert_to_tensor(i_vecs, dtype=tf.float32), tf.convert_to_tensor(i_biases, dtpye=tf.float32))
            )


    def _loss(self, y_pred, y_true, batch_ids: Tuple[tf.Tensor, tf.Tensor] | None, use_l2: bool = False):
        assert tf.shape(y_pred)[0] == tf.shape(y_true)[0]

        loss = tf.math.square(y_pred - y_true) / tf.shape(y_true)[0]

        if use_l2:
            u_ids, i_ids = batch_ids
            u_vecs, _ = self.u_latent.forward(u_ids)
            i_vecs, _ = self.i_latent.forward(i_ids)
            loss += self._lambda * (tf.reduce_sum(tf.math.square(u_vecs)) + tf.reduce_sum(i_vecs))
        return loss


    def simple_fit(self, x_train, y_train, num_epochs=2, batch_size: int = 40, shuffle=False, random_seed=41,
                use_l2: bool = False) -> Any:
        tf.random.set_seed(random_seed)

        losses = tf.TensorArray(dtype=tf.float32, size=num_epochs)
        ds_train = tf.data.Dataset.from_tensor_slices((x_train, y_train))
        for epoch in range(num_epochs):
            epoch_losses = []
            ds_batched = x_train.shuffle(buffer_size=batch_size << 3).batch(batch_size).cache().prefetch(tf.data.AUTOTUNE)
            for i, x_y in enumerate(ds_batched):
                x_batch, y_batch = x_y
                with tf.GradientTape(persistent=True) as tape:
                    self.u_latent.monitor_variables(tape)
                    self.i_latent.monitor_variables(tape)

                    y_pred = self.forward(x_batch, training=True)

                    loss = self._loss(y_pred, y_batch, use_l2)
                    epoch_losses.append(loss)

                    if (i + 1) % 50 == 0:
                        print(f"Epoch: {epoch} - Step: {i} - Loss: {loss.numpy()}")

                self.u_latent.simple_backward(tape, loss, x_batch[:, 0])
                self.i_latent.simple_backward(tape, loss, x_batch[:, 1])

            losses.write(epoch, tf.constant(epoch_losses))
            print(f"----------------------------------End| |Epoch={epoch}| |End----------------------------")

         return losses