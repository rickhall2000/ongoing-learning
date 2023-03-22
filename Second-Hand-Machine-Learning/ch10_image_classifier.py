import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
from time import strftime

fashion_mnist = tf.keras.datasets.fashion_mnist.load_data()
(X_train_full, y_train_full), (X_test, y_test) = fashion_mnist

X_train, y_train = X_train_full[:-5000], y_train_full[:-5000]
X_valid, y_valid = X_train_full[-5000:], y_train_full[-5000:]

X_train, X_valid, X_test = X_train / 255., X_valid / 255., X_test / 255.

class_names = ["T-shirt/top", "Trouser", "pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]


def get_run_logdir(root_logdir="my_logs"):
    return Path(root_logdir) / strftime("run_%Y_%m_%d_%H_%M_%s")


def build_model():
    tf.random.set_seed(42)
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Input(shape=[28,28]))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(300, activation="relu", name="first_dense"))
    model.add(tf.keras.layers.Dense(100, activation="relu", name="second_dense"))
    model.add(tf.keras.layers.Dense(10, activation="softmax"))
    return model


def compile_model(model):
    model.compile(loss="sparse_categorical_crossentropy",
                  optimizer="sgd",
                  metrics=["accuracy"])


def train_model(model, epochs=30):
    run_logdir = get_run_logdir()
    tensorboard_cb = tf.keras.callbacks.TensorBoard(run_logdir,
                                                    profile_batch=(0, epochs))
    hist = model.fit(X_train, y_train, epochs=epochs,
                     validation_data=(X_valid, y_valid),
                     callbacks=[tensorboard_cb]
                     )
    return hist


def plot_history(history):

    pd.DataFrame(history.history).plot(
        figsize=(8,5), xlim=[0,29], ylim=[0,1], grid=True, xlabel="Epoch",
        style=["r--", "r--.", "b-", "b-*"])
    plt.show()


def evaluate_model(model):
    return model.evaluate(X_test, y_test)


def new_predictions(model):
    X_new = X_test[:3] # using first 3 training examples because we don't really have new examples
    y_proba = model.predict(X_new)
    print(y_proba.round(2))
    y_pred = y_proba.argmax(axis=-1)
    print(y_pred)
    print(np.array(class_names)[y_pred])


def kick_it_off():
    m = build_model()
    compile_model(m)
    h = train_model(m, 50)
    print(evaluate_model(m))
    plot_history(h)
    new_predictions(m)


def plot_image(which=0):
    example = X_train_full[which]
    plt.imshow(example, cmap="gray")
    plt.show()


kick_it_off()