import csv
import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

train_path = "datasets/jsb_chorales/train"
test_path = "datasets/jsb_chorales/test"
valid_path = "datasets/jsb_chorales/valid"

sequence_length = 16
batch_size = 32

def list_files(path):
    filenames = os.listdir(path)
    return [os.path.join(path, filename) for filename in filenames]

def load_file(filename):
    rows = []
    with open(filename) as source_file:
        csv_reader = csv.reader(source_file)
        next(csv_reader)
        for row in csv_reader:
            row_func = lambda x: float(x) / 100.0
            elements = list(map(row_func, row))
            rows.append(elements)
    return np.array(rows)

# Need to take in an array, and return a bunch of batches
def windowing_function(array):
    return tf.keras.utils.timeseries_dataset_from_array(
            array,
            targets=array[:sequence_length],
            sequence_length=sequence_length,
            batch_size=batch_size,
        )

def gimmie_data(path):
    files = list_files(path)
    all_data = None
    for file in files:
        data = load_file(file)
        if all_data:
            all_data.concatenate(windowing_function(data))
        else:
            all_data = windowing_function(data)

    return all_data

# I should be able to train a simple model on that one data set
def build_model():
    tf.keras.backend.clear_session()
    model = tf.keras.Sequential([
        tf.keras.layers.Conv1D(32, kernel_size=4),
        tf.keras.layers.LSTM(32, return_sequences=True),
        tf.keras.layers.LSTM(32),
        tf.keras.layers.Dense(4, activation="relu")
    ])
    optimizer="Adam"
    model.compile(optimizer=optimizer, loss=tf.keras.losses.Huber(), metrics=["mae"])
    return model

def train_model(model, data, validation):
    history = model.fit(data, epochs=20, validation_data=validation)
    return history

def plot_results(hist):
    error = hist.history["mae"]
    valid_error = hist.history["val_mae"]
    plt.plot(error, color="b")
    plt.plot(valid_error, color="r")
    plt.show()

def do_the_thing():
    train_data = gimmie_data(train_path)
    valid_data = gimmie_data(valid_path)
    model = build_model()
    history = train_model(model, train_data, valid_data)
    plot_results(history)
    return model, history

