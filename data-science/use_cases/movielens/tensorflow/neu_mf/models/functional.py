from typing import List

import numpy as np
from keras import Input
from tensorflow.keras.layers import Embedding, Dense, Embedding, StringLookup, Flatten, Dropout, Concatenate, Lambda
from tensorflow.keras.models import Model
import tensorflow as tf
from tensorflow.keras.regularizers import l2
from tensorflow.keras.initializers import RandomNormal


def hadamard_product(stuffs):
    P, Q = stuffs

    return tf.math.multiply(P, Q)


def build_embedding_layer(input_l,embedding_dim: int, vocab: np.ndarray,name: str, has_l2_reg=False):

    n_vocab = vocab.shape[0]

    string_lookup_l = StringLookup(vocabulary=vocab, name=f"{name}_string_lookup")(input_l)
    embed_l = Embedding(input_dim=n_vocab+1, output_dim=embedding_dim,
                        embeddings_initializer=RandomNormal(stddev=0.01),
                        embeddings_regularizer=l2() if has_l2_reg else None,
                        trainable=True, name=f"{name}_embedding")(string_lookup_l)

    return embed_l



def build_neu_mf_model(user_vocab: set, item_vocab: set, embedding_dim: int, hidden_num: int, hidden_dim: List[int]):
    user_vocab = np.array(user_vocab)
    item_vocab = np.array(item_vocab)

    user_input = Input(shape=(None,), dtype=tf.string, name='user_input')
    item_input = Input(shape=(None,), dtype=tf.string, name='item_input')

    # user embedding

    P = build_embedding_layer(user_input, embedding_dim=embedding_dim, vocab=user_vocab, name='user_P', has_l2_reg=True)
    Q = build_embedding_layer(item_input, embedding_dim=embedding_dim, vocab=item_vocab, name='item_Q', has_l2_reg=True)

    U = build_embedding_layer(user_input, embedding_dim=embedding_dim, vocab=user_vocab, name='user_U', has_l2_reg=True)
    V = build_embedding_layer(item_input, embedding_dim=embedding_dim, vocab=item_vocab, name='item_V', has_l2_reg=True)

    concatenate_l = Concatenate( name="concatenate_U_V")([U, V])

    hidden_l = Dense(units= hidden_dim[0], activation="relu", name="hidden_l_0")(concatenate_l)

    for i in range(1, hidden_num):
        hidden_l = Dense(units= hidden_dim[i], activation="relu", name="hidden_l_{}".format(i))(hidden_l)

    element_wise_prod = Lambda(hadamard_product, name="element_wise_prod")([P, Q])

    final_concat = Concatenate(name="concat_of_last_hidden_with_P_x_Q")([hidden_l, element_wise_prod])

    output_l = Dense(units=1, activation=None, name="output_l", use_bias=False)(final_concat)

    model = Model(inputs=[user_input, item_input], outputs=output_l)

    return model



