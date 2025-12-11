from build_models_with_frameworks.movielens.tensorflow.mf.model import MatrixFactorizationModel
import tensorflow as tf
import numpy as np

def setup_mf_model(embedding_dims, num_users, num_items,user_vocab, item_vocab, lr = 0.002):
    model = MatrixFactorizationModel(embedding_dims, num_users, num_items, user_vocab, item_vocab)

    model.compile(loss = tf.keras.losses.MeanSquaredError(),
                  optimizer = tf.keras.optimizers.Adam(learning_rate = 0.002),
                  metrics = [tf.keras.metrics.RootMeanSquaredError()])
    return model


def oo_train_mf_model(mf_model, df, num_epochs=2, checkpoint_path="/kaggle/working/models"
                      , log_dir="/kaggle/working/logs/",
                      split_ratio=0.9, batch_size=2):
    X_data = df[["user_id", "item_id"]].to_numpy()
    Y_data = np.squeeze(df[["rating"]].to_numpy())

    n = X_data.shape[0]

    train_size = int(n * split_ratio)

    dataset = tf.data.Dataset.from_tensor_slices((X_data, Y_data)).shuffle(n)

    train_dataset = dataset.take(train_size)
    val_dataset = dataset.skip(train_size)

    train_dataset = train_dataset.shuffle(batch_size << 2).batch(batch_size).cache().prefetch(tf.data.AUTOTUNE)
    val_dataset = val_dataset.batch(batch_size).cache().prefetch(tf.data.AUTOTUNE)

    # callbacks
    log_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path)
    earlystopping_callback = tf.keras.callbacks.EarlyStopping()

    history = mf_model.fit(train_dataset,
                           epochs=num_epochs,
                           validation_data=val_dataset,
                           callbacks=[log_callback, checkpoint_callback, earlystopping_callback])
    return history
