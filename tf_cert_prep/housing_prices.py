import sys

import tensorflow as tf
import numpy as np

def house_model():
    xs = np.array([1, 2, 3, 4, 5, 6], dtype="float")
    ys = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5], dtype=float)

    model = tf.keras.Sequential(tf.keras.layers.Dense(1, input_shape=[(1)]))

    model.compile(optimizer="SGD", loss="MeanSquaredError")

    model.fit(xs, ys, epochs=1000)
    return model

model = house_model()

new_y = 7.0
prediction = model.predict([new_y])[0]
print(sys.version)
print(prediction)