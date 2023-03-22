import tensorflow as tf
import keras_tuner as kt
from pathlib import Path


fashion_mnist = tf.keras.datasets.fashion_mnist.load_data()
(X_train_full, y_train_full), (X_test, y_test) = fashion_mnist

X_train, y_train = X_train_full[:-5000], y_train_full[:-5000]
X_valid, y_valid = X_train_full[-5000:], y_train_full[-5000:]

X_train, X_valid, X_test = X_train / 255., X_valid / 255., X_test / 255.


def build_model(hp):
    n_hidden = hp.Int("n_hidden", min_value=0, max_value=8, default=2)
    n_neurons = hp.Int("n_neurons", min_value=16, max_value=256)
    learning_rate = hp.Float("learning_rate", min_value=1e-4, max_value=1e-2,
                             sampling="log")
    optimizer = hp.Choice("optimizer", values=["sgd", "adam"])
    if optimizer == "sgd":
        optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate)
    else:
        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Flatten())
    for _ in range(n_hidden):
        model.add(tf.keras.layers.Dense(n_neurons, activation="relu"))
    model.add(tf.keras.layers.Dense(10, activation="softmax"))
    model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer,
                  metrics=["accuracy"])
    return model

def random_search():
    random_search_tuner = kt.RandomSearch(
        build_model, objective="val_accuracy", max_trials=10, overwrite=False,
        directory="my_fashion_mnist", project_name="my_rnd_search", seed=42)
    random_search_tuner.search(X_train, y_train, epochs=10, validation_data=(X_valid, y_valid))

    print("About to get best trial")
    best_trial = random_search_tuner.oracle.get_best_trials(num_trials=1)[0]
    print(best_trial.summary())
    print(best_trial.metrics.get_last_value("val_accuracy"))

    print("About to get best model")
    top3_models = random_search_tuner.get_best_models(num_models=3)
    best_model = top3_models[0]
    print(best_model)

    print("About to get best params")
    top3_params = random_search_tuner.get_best_hyperparameters(num_trials=3)
    print(top3_params[0].values)

    print("Let's continue training")
    best_model.fit(X_train_full, y_train_full, epochs=10)
    print(best_model.evaluate(X_test, y_test))


# If you want to add tunable preprocessing you need a custom fit function
class MyClassificationHyperModel(kt.HyperModel):
    def build(self, hp):
        return build_model(hp)

    def fit(self, hp, model, X, y, **kwargs):
        if hp.Boolean("normalize"):
            norm_layer = tf.keras.layers.Normalization()
            X = norm_layer(X)
        return model.fit(X, y, **kwargs)


def hyperband():
    hyperband_tuner = kt.Hyperband(
        MyClassificationHyperModel(), objective="val_accuracy", seed=42,
        max_epochs=10, factor=3, hyperband_iterations=2,
        overwrite=True, directory="my_fashion_mnist", project_name="hyberband"
    )

    root_logdir = Path(hyperband_tuner.project_dir) / "tensorboard"
    early_stopping_cb = tf.keras.callbacks.EarlyStopping(patience=2)
    tensorboard_cb = tf.keras.callbacks.TensorBoard(root_logdir)
    hyperband_tuner.search(X_train, y_train, epochs=10,
                           validation_data=(X_valid, y_valid),
                           callbacks=[early_stopping_cb, tensorboard_cb])


def bayesian():
    bayseian_opt_tuner = kt.BayesianOptimization(
        MyClassificationHyperModel(), objective="val_accuracy", seed=42,
        max_trials=10, alpha=1e-4, beta=2.6,
        overwrite=True, directory="my_fashion_mndist", project_name="baysian_opt"
    )
    bayseian_opt_tuner.search([...])