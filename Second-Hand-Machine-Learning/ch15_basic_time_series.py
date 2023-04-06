import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import tensorflow as tf

seq_length = 56


def get_rider_data():
    ridership_file = "datasets/CTA_-_Ridership_-_Daily_Boarding_Totals.csv"
    path = Path(ridership_file)
    df = pd.read_csv(path, parse_dates=["service_date"])
    df.columns = ["date", "day_type", "bus", "rail", "total"]
    df = df.sort_values("date").set_index("date")
    df = df.drop("total", axis=1)
    return df


def diff_7(df):
    diff_7 = df[["bus", "rail"]].diff(7)["2019-03":"2019-05"]

    fig, axs = plt.subplots(2, 1, sharex=True, figsize=(8,5))
    df.plot(ax=axs[0], legend=False, marker=".")
    df.shift(7).plot(ax=axs[0], grid=True, legend=False, linestyle=":")
    diff_7.plot(ax=axs[1], grid=True, marker=".")
    plt.show()
    return diff_7


def sample_series():
    my_series = [0, 1, 2, 3, 4, 5]
    my_dataset = tf.keras.utils.timeseries_dataset_from_array(
        my_series,
        targets=my_series[3:],
        sequence_length=3,
        batch_size=2
    )
    return my_dataset


def sample_window():
    for window_dataset1 in tf.data.Dataset.range(6).window(4, shift=1):
        for element in window_dataset1:
            print(f"{element}", end=" ")
        print()

    dataset = tf.data.Dataset.range(6).window(4, shift=1, drop_remainder=True)
    dataset = dataset.flat_map(lambda window_dataset: window_dataset.batch(4))
    for window_tensor in dataset:
        print(f"{window_tensor}")


def to_windows(dataset, length):
    dataset = dataset.window(length, shift=1, drop_remainder=True)
    return dataset.flat_map(lambda window_ds: window_ds.batch(length))


def make_sample_dataset():
    dataset = to_windows(tf.data.Dataset.range(6), 4) # 3 inputs + 1 target
    dataset = dataset.map(lambda window: (window[:-1], window[-1]))
    return dataset



def make_rail_datasets():
    df = get_rider_data()
    rail_train = df["rail"]["2016-01":"2018-12"] / 1e6
    rail_valid = df["rail"]["2019-01":"2019-05"] / 1e6
    rail_test =  df["rail"]["2019-06":] / 1e6

    train_ds = tf.keras.utils.timeseries_dataset_from_array(
        rail_train.to_numpy(),
        targets=rail_train[seq_length:],
        sequence_length=seq_length,
        batch_size=32,
        shuffle=True,
        seed=42
    )
    valid_ds = tf.keras.utils.timeseries_dataset_from_array(
        rail_valid.to_numpy(),
        targets=rail_valid[seq_length:],
        sequence_length=seq_length,
        batch_size=32
    )

    return train_ds, valid_ds


def forecast_any_model(model):
    train_ds, valid_ds = make_rail_datasets()
    tf.random.set_seed(42)
    early_stopping_cb = tf.keras.callbacks.EarlyStopping(
        monitor="val_mae", patience=50, restore_best_weights=True)
    opt = tf.keras.optimizers.SGD(learning_rate=0.02, momentum=0.9)
    model.compile(loss=tf.keras.losses.Huber(), optimizer=opt, metrics=["mae"])
    history = model.fit(train_ds, validation_data=valid_ds, epochs=500,
                        callbacks=[early_stopping_cb])
    return history, model


def forecast_linear_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(1, input_shape=[seq_length])
    ])
    return forecast_any_model(model)


def forecast_simple_rnn():
    model = tf.keras.Sequential([
        tf.keras.layers.SimpleRNN(1, input_shape=[None, 1])
    ])
    return forecast_any_model(model)


def forecast_univar_rnn():
    model = tf.keras.Sequential([
        tf.keras.layers.SimpleRNN(32, input_shape=[None, 1]),
        tf.keras.layers.Dense(1)
    ])
    return forecast_any_model(model)

def forecast_deep_rnn():
    model = tf.keras.Sequential([
        tf.keras.layers.SimpleRNN(32, return_sequences=True, input_shape=[None, 1]),
        tf.keras.layers.SimpleRNN(32, return_sequences=True),
        tf.keras.layers.SimpleRNN(32),
        tf.keras.layers.Dense(1)
    ])
    return forecast_any_model(model)

def multivar_data():
    df = get_rider_data()
    df_mulvar = df[["bus", "rail"]] / 1e6
    df_mulvar["next_day_type"] = df["day_type"].shift(-1)
    df_mulvar = pd.get_dummies(df_mulvar)
    
    mulvar_train = df_mulvar["2016-01":"2018-12"]
    mulvar_valid = df_mulvar["2019-01":"2019-05"]
    mulvar_test = df_mulvar["2019-06":]

    train_mulvar_ds = tf.keras.utils.timeseries_dataset_from_array(
        mulvar_train.to_numpy(),
        targets=mulvar_train[["rail", "bus"]][seq_length:],
        sequence_length=seq_length,
        batch_size=32,
        shuffle=True,
        seed=42
    )

    valid_mulvar_ds = tf.keras.utils.timeseries_dataset_from_array(
        mulvar_valid.to_numpy(),
        targets=mulvar_valid[["rail", "bus"]][seq_length:],
        sequence_length=seq_length,
        batch_size=32
    )

    return train_mulvar_ds, valid_mulvar_ds

def train_multi_var_rnn():
    train_ds, valid_ds = multivar_data()
    model = tf.keras.Sequential([
        tf.keras.layers.SimpleRNN(32, input_shape=[None, 5]),
        tf.keras.layers.Dense(2)
    ])
    tf.random.set_seed(42)
    early_stopping_cb = tf.keras.callbacks.EarlyStopping(
        monitor="val_mae", patience=50, restore_best_weights=True)
    opt = tf.keras.optimizers.SGD(learning_rate=0.02, momentum=0.9)
    model.compile(loss=tf.keras.losses.Huber(), optimizer=opt, metrics=["mae"])
    history = model.fit(train_ds, validation_data=valid_ds, epochs=500,
                        callbacks=[early_stopping_cb])
    predictions = model.predict(valid_ds)

    return predictions

