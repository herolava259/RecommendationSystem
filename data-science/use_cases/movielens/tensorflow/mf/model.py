import tensorflow as tf
from tensorflow.keras.initializers import RandomNormal
from typing import Union, Set, List
import tensorflow as tf

from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Embedding, StringLookup, Flatten, Lambda
from tensorflow.keras.regularizers import L2
import numpy as np


# object oriented model
class MatrixFactorizationModel(tf.keras.Model):
    def __init__(self, embedding_dims: int,
                 num_users: int, num_items: int,
                 user_vocab: Union[Set[str], List[str], np.ndarray],
                 item_vocab: Union[Set[str], List[str], np.ndarray],
                 **kwargs):
        super().__init__()

        if isinstance(user_vocab, set):
            user_vocab = np.array(user_vocab)
        elif isinstance(user_vocab, list) or isinstance(user_vocab, np.ndarray):
            user_vocab = np.unique(user_vocab)

        if isinstance(item_vocab, set):
            item_vocab = np.array(item_vocab)
        elif isinstance(item_vocab, list) or isinstance(item_vocab, np.ndarray):
            item_vocab = np.unique(item_vocab)

        self.user_embedding = tf.keras.Sequential([
            tf.keras.layers.StringLookup(vocabulary=user_vocab,
                                         mask_token=None, ),
            tf.keras.layers.Embedding(num_users, embedding_dims,
                                      embeddings_initializer=RandomNormal(stddev=0.01), trainable=True)
        ])
        self.item_embedding = tf.keras.Sequential([
            tf.keras.layers.StringLookup(vocabulary=item_vocab,
                                         mask_token=None, ),
            tf.keras.layers.Embedding(num_items, embedding_dims,
                                      embeddings_initializer=RandomNormal(stddev=0.01), trainable=True)
        ])

        self.user_bias = tf.keras.Sequential([
            tf.keras.layers.StringLookup(vocabulary=user_vocab,
                                         mask_token=None, ),
            tf.keras.layers.Embedding(num_users, 1, embeddings_initializer=RandomNormal(stddev=0.01), trainable=True),
            tf.keras.layers.Flatten()
        ], trainable=True, name="user_bias")

        self.item_bias = tf.keras.Sequential([
            tf.keras.layers.StringLookup(vocabulary=item_vocab,
                                         mask_token=None, ),
            tf.keras.layers.Embedding(num_items, 1, embeddings_initializer=RandomNormal(stddev=0.01), trainable=True),
            tf.keras.layers.Flatten()
        ], trainable=True, name="item_bias")

    def call(self, X):

        user_id = X[0]
        item_id = X[1]

        Q = self.user_embedding(user_id)
        bq = self.user_bias(user_id)

        I = self.item_embedding(item_id)
        bi = self.item_bias(item_id)

        # print("Q= ", Q)
        # print("I= ", I)

        # print("bq= ", bq)
        # print("bi= ", bi)

        # tf.print("Q= ", Q)
        # tf.print("I= ", I)

        # tf.print("bq= ", bq)
        # tf.print("bi= ", bi)

        # product of two vectors Q and I (Q.I)
        # tf.einsum("i,i->", Q, I)
        # tf.tensordot(Q, I, 1)
        # tf.matmul(Q, tf.transpose(I)) => not working

        return tf.reduce_sum(tf.multiply(Q, I)) + bq + bi



# sequential functional api

def product_of_two_embeddings(stuffs):
    Q, bq, I, bi = stuffs
    return tf.reduce_sum(tf.multiply(Q, I)) + bq + bi


def initialize_embedding_model(embedding_dims: int, vocab: np.ndarray, has_l2_reg=False):
    n_vocab = vocab.shape[0]
    print("n_vocab = ", n_vocab)
    input_model = Input(shape=(1,), dtype=tf.string)
    embed_model = StringLookup(vocabulary=vocab, mask_token=None)(input_model)
    embed_model = Embedding(input_dim=n_vocab + 1, output_dim=embedding_dims,
                            embeddings_initializer=RandomNormal(stddev=0.01),
                            embeddings_regularizer=L2() if has_l2_reg else None,
                            trainable=True)(embed_model)
    bias_model = StringLookup(vocabulary=vocab, mask_token=None)(input_model)
    bias_model = Embedding(input_dim=n_vocab + 1, output_dim=1,
                           embeddings_initializer=RandomNormal(stddev=0.01),
                           embeddings_regularizer=L2() if has_l2_reg else None,
                           trainable=True)(bias_model)
    bias_model = Flatten()(bias_model)

    return input_model, embed_model, bias_model


def fn_api_build_mf_model(embedding_dims: int, user_vocab: np.ndarray, item_vocab: np.ndarray,
                          has_l2_reg: bool = False):
    user_input, user_embed, user_bias = initialize_embedding_model(embedding_dims, user_vocab, has_l2_reg)
    item_input, item_embed, item_bias = initialize_embedding_model(embedding_dims, item_vocab, has_l2_reg)

    output_model = Lambda(product_of_two_embeddings)([user_embed, user_bias, item_embed, item_bias])

    model = Model(inputs=[user_input, item_input], outputs=output_model)

    return model



