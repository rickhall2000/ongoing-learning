import tensorflow as tf
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

housing = fetch_california_housing()
X_train_full, X_test, y_train_full, y_test = train_test_split(
    housing.data, housing.target, random_state=42)
X_train, X_valid, y_train, y_valid = train_test_split(
    X_train_full, y_train_full, random_state=42)

def regression():
    tf.random.set_seed(42)
    norm_layer = tf.keras.layers.Normalization(input_shape=X_train.shape[1:])
    model = tf.keras.Sequential([
        norm_layer,
        tf.keras.layers.Dense(50, activation="relu"),
        tf.keras.layers.Dense(50, activation="relu"),
        tf.keras.layers.Dense(50, activation="relu"),
        tf.keras.layers.Dense(1)
    ])
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
    model.compile(loss="mse", optimizer=optimizer, metrics=["RootMeanSquaredError"])
    norm_layer.adapt(X_train)
    history = model.fit(X_train, y_train, epochs=20,
                        validation_data=(X_valid, y_valid))
    mse_test, rmse_test = model.evaluate(X_test, y_test)
    X_new = X_test[:3]
    y_pred = model.predict(X_new)
    print(mse_test, rmse_test)

def wide_and_deep():
    norm_layer = tf.keras.layers.Normalization()
    hidden_layer1 = tf.keras.layers.Dense(30, activation="relu")
    hidden_layer2 = tf.keras.layers.Dense(30, activation="relu")
    concat_layer = tf.keras.layers.Concatenate()
    output_layer = tf.keras.layers.Dense(1)

    input_ = tf.keras.layers.Input(shape=X_train.shape[1:])
    normalized = norm_layer(input_)
    hidden1 = hidden_layer1(normalized)
    hidden2 = hidden_layer2(hidden1)
    concat = concat_layer([normalized, hidden2])
    output = output_layer(concat)

    model = tf.keras.Model(inputs=[input_], outputs=[output])
    print(model.summary())


def multi_path():
    input_wide = tf.keras.layers.Input(shape=[5])
    input_deep = tf.keras.layers.Input(shape=[6])
    norm_layer_wide = tf.keras.layers.Normalization()
    norm_layer_deep = tf.keras.layers.Normalization()
    norm_wide = norm_layer_wide(input_wide)
    norm_deep = norm_layer_deep(input_deep)

    hidden1 = tf.keras.layers.Dense(30, activation="relu")(norm_deep)
    hidden2 = tf.keras.layers.Dense(30, activation="relu")(hidden1)

    concat = tf.keras.layers.concatenate([norm_wide, hidden2])
    output = tf.keras.layers.Dense(1)(concat)
    model = tf.keras.Model(inputs=[input_wide, input_deep], outputs=[output])
    print(model.summary())

    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
    model.compile(loss="mse", optimizer=optimizer, metrics=["RootMeanSquaredError"])

    X_train_wide, X_train_deep = X_train[:, :5], X_train[:, 2:]
    X_valid_wide, X_valid_deep = X_valid[:, :5], X_valid[:, 2:]
    X_test_wide, X_test_deep = X_test[:, :5], X_test[:, 2:]
    X_new_wide, X_new_deep = X_test_wide[:3], X_test_deep[:3]

    # Have to call adapt on normalization layers before fitting model
    norm_layer_wide.adapt(X_train_wide)
    norm_layer_deep.adapt(X_train_deep)

    history = model.fit((X_train_wide, X_train_deep), y_train, epochs=20,
                        validation_data=((X_valid_wide, X_valid_deep), y_valid))

    mse_test = model.evaluate((X_test_wide, X_test_deep), y_test)
    print(mse_test)

def multi_output():
    input_wide = tf.keras.layers.Input(shape=[5])
    input_deep = tf.keras.layers.Input(shape=[6])
    norm_layer_wide = tf.keras.layers.Normalization()
    norm_layer_deep = tf.keras.layers.Normalization()
    norm_wide = norm_layer_wide(input_wide)
    norm_deep = norm_layer_deep(input_deep)

    hidden1 = tf.keras.layers.Dense(30, activation="relu")(norm_deep)
    hidden2 = tf.keras.layers.Dense(30, activation="relu")(hidden1)

    concat = tf.keras.layers.concatenate([norm_wide, hidden2])

    # 2 outputs
    output = tf.keras.layers.Dense(1)(concat)
    aux_output = tf.keras.layers.Dense(1)(hidden2)
    model = tf.keras.Model(inputs=[input_wide, input_deep], outputs=[output, aux_output])
    print(model.summary())

    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)

    # need 2 loss functions for the two outputs
    model.compile(loss=("mse", "mse"), loss_weights=(0.9, 0.1),
                  optimizer=optimizer, metrics=["RootMeanSquaredError"])

    X_train_wide, X_train_deep = X_train[:, :5], X_train[:, 2:]
    X_valid_wide, X_valid_deep = X_valid[:, :5], X_valid[:, 2:]
    X_test_wide, X_test_deep = X_test[:, :5], X_test[:, 2:]
    X_new_wide, X_new_deep = X_test_wide[:3], X_test_deep[:3]

    # Have to call adapt on normalization layers before fitting model
    norm_layer_wide.adapt(X_train_wide)
    norm_layer_deep.adapt(X_train_deep)

    # need to pass 2 targets, for the 2 outputs
    history = model.fit((X_train_wide, X_train_deep), (y_train, y_train), epochs=20,
                        validation_data=((X_valid_wide, X_valid_deep), (y_valid, y_valid)))

    eval_results = model.evaluate((X_test_wide, X_test_deep), (y_test, y_test))
    print(eval_results)

    y_pred_tuple = model.predict((X_new_wide, X_new_deep))
    y_pred = dict(zip(model.output_names, y_pred_tuple))
    print(y_pred)

multi_output()