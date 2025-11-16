from abc import ABC, abstractmethod
from typing import List, Set, Any, Tuple

from tensorflow import Module, GradientTape
from tensorflow.keras.optimizers import Optimizer
from tensorflow.keras.initializers import RandomNormal, Zeros

import tensorflow as tf



class RecLayer(Module):

    @abstractmethod
    def forward(self, inputs, training: bool = False) -> tf.Tensor | Any:
        pass

    @abstractmethod
    def backward_with_optimizer(self, tape: GradientTape, loss: Any, optimizer: Optimizer | None = None):
        pass

    @abstractmethod
    def backward(self, tape: GradientTape, loss: Loss, lr: float = 0.002):
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


class RecEmbeddingLayer(RecLayer):
    def __init__(self, vocab: List[str] | Set[str], embedding_dim: int, **kwargs):
        kwargs["trainable"] = True
        kwargs["dtype"] = tf.float
        super().__init__(RecEmbeddingLayer, self).__init__(**kwargs)
        self.vocab = tf.constant(vocab, dtype=tf.string)
        self.embedding_dim = embedding_dim
        self.n_space = tf.shape(self.vocab)[0]
        self.name2ids = None
        self.embed_vars = None
        self.bias = None
        self.embed_oov = None
        self.bias_oov = None

    def initialize(self, **kwargs):
        ids = tf.range(start=0, limit=self.n_item, delta=1, name=f"{self.name}-range")

        self.name2ids = tf.lookup.StaticHashTable(initializer=tf.lookup.KeyValueTensorInitializer(self.vocab, ids),
                                                  key_dtype=tf.string, value_dtype=tf.int32, default_value="OOV")

        w_initializer = RandomNormal(std=0.01)
        b_initializer = Zeros()

        self.embed_vars = [tf.Variable(w_initializer(shape=(self.embedding_dim)), dtype=tf.float32, trainable=True) for
                           _ in range(self.n_space)]
        self.bias = tf.Variable(b_initializer(shape=(self.n_space, 1)), dtype=tf.float32, trainable=True)

        self.embed_oov = tf.constant(w_initializer(shape=(self.embedding_dim,)), dtype=tf.float32)
        sekf.bias_oov = tf.constant(w_initializer(shape=(1,)), dtype=tf.float32)

    def _forward_batch_training(self, inputs: tf.Tensor):
        extr_ids = tf.sparse.to_dense(self.name2ids.lookup(inputs))
        # assert all identifiers in vocab
        # end assert
        extr_ids = tf.sparse.to_dense(self.name2ids.lookup(inputs))

        return tf.gather(self.embed_vars, extr_ids, axis=0), tf.gather(self.bias, extr_ids, axis=0)

    def _forward_batch_predict(self, inputs: tf.Tensor):
        # out of vocab index
        extr_ids = tf.sparse.to_dense(self.name2ids.lookup(inputs))

        # rerieve ids of ids in vocabulary

        length = tf.shape[]

        beg_emb = self.embed_vecs[extr_ids[0]] if extr_ids[0] != -1 else self.embed_oov
        beg_bias = self.bias[extr_ids[0]] if extr_ids[0] != -1 else self.bias_oov[0]

        beg_embs = tf.expand_dims(beg_emb, axis=0)
        beg_biaes = tf.expand_dims(beg_bias, axis=0)

        def loop_body_vec(i, tensor_grow):

            concated_vec = self.embed_oov

            if extr_ids[i] != -1:
                concated_vec = self.embed_vecs[extr_ids[i]]

            return i + 1, tf.concat(values=[tensor_grow, tf.expand_dims(concated_vec, axis=0)])

        def loop_body_bias(i, tensor_grow):
            concated_bias = self.bias_oov[0]

            if extr_ids[i] != -1:
                concated_bias = self.bias[extr_ids[i]]
            return i + 1, tf.concat(values=[tensor_grow, tf.expand_dims(concated_bias, axis=0)])

        _, embed_result = tf.while_loop(lambda i, tensor_grow: i < length, loop_body_vec,
                                        [tf.constant(1, dtype=tf.int64), beg_embs])

        _, bias_result = tf.while_loop(lambda i, tensor_grow: i < length, loop_body_bias,
                                       [tf.constant(1, dtype=tf.int64), beg_biaes])

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
        tape.watch(self.embed_vecs)
        tape.watch(self.bias)

    def get_variable(self) -> Tuple[tf.Variable, tf.Variable]:
        return self.embed_vecs, self.bias

    def backward(self, tape: GradientTape, loss: Any, lr: float = 0.002):
        embed_grad = tape,

    def backward_with_optimizer(self, tape: GradientTape, loss: Any, optimizer: Optimizer | None = None):


class FineGrainedMFModel(Module):
    def __init__(self, user_vocab, item_vocab, embedding_dim):
        self.user_vocab = tf.constant(user_vocab, dtype=tf.string)
        self.item_vocab = tf.constant(item_vocab, dtype=tf.string)
        self.embedding_dim = embedding_dim

        self.n_item = self.user_vocab.shape[0]
        self.n_user = self.item_vocab.shape[0]

        item_range = tf.range(start=0, limit=self.n_item, delta=1, name="item-range")
        user_range = tf.range(start=0, limit=self.n_user, delta=1, name="user-range")

        self.item2ids = tf.lookup.StaticHashTable(
            initializer=tf.lookup.KeyValueTensorInitializer(self.item_vocab, item_range),
            key_dtype=tf.string, value_dtype=tf.int32, default_value="OOV")
        self.user2ids = tf.lookup.StaticHashTable(
            initializer=tf.lookup.KeyValueTensorInitializer(self.user_vocab, user_range),
            key_dtype=tf.string, value_dtype=tf.int32, default_value="OOV")

        ## emebding vectors

# TODO: Change tensor of embedding space to list of embedding vectors




