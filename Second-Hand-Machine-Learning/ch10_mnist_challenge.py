import tensorflow as tf
import matplotlib.pyplot as plt

(X_train_full, y_train_full), (X_test, y_test) = tf.keras.datasets.mnist.load_data()

X_train, X_valid = X_train_full[:-10000], X_train_full[-10000:]
y_train, y_valid = y_train_full[:-10000], y_train_full[-10000:]


# ok, I have split my data, now I need to build a model
def build_model(learning_rate=0.01):
    model = tf.keras.Sequential([
                tf.keras.layers.Input(shape=(28,28)),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(50, activation="relu"),
                tf.keras.layers.Dense(50, activation="relu"),
                tf.keras.layers.Dense(50, activation="relu"),
                tf.keras.layers.Dense(10, activation="softmax")
            ])
    optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate)
#    optimizer = tf.keras.optimizers.Adam()
    model.compile(optimizer=optimizer, loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


def train_model(model, epochs=5):
    early_stopping_cb = tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)
    history = model.fit(X_train, y_train, validation_data=(X_valid, y_valid), epochs=epochs,
                        batch_size=20, callbacks=[early_stopping_cb])
    return history


def plot_results(history, learning_rate):
    loss, accuracy, val_loss, val_accuracy = history.history["loss"], history.history["accuracy"], \
                                             history.history["val_loss"], history.history["val_accuracy"]
    plt.plot(accuracy, color="b")
    plt.plot(val_accuracy, color="r")
    plt.title(learning_rate)
    plt.show()


def run_test(learning_rate=0.01, epochs=5, plot=True):
    m = build_model(learning_rate)
    h = train_model(m, epochs)
    if plot:
        plot_results(h, learning_rate)
    final_accuracy = h.history["val_accuracy"][-1]
    return final_accuracy


def run_many_tests():
    learning_rates = [0.005, 0.001, 0.0005]
    results = {}
    for lr in learning_rates:
        print("Trying learning rate: ", lr)
        score = run_test(lr, 10, False)
        results[lr] = score
    print(results)


def final_training():
    learning_rate = 0.001
    m = build_model(learning_rate)
    h = train_model(m, 100)
    plot_results(h, learning_rate)
    m.save("mnist_model.h5")
    print(m.evaluate(X_test, y_test))
    return m, h
