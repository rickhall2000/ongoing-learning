import matplotlib.pyplot as plt
import tensorflow as tf
import csv
import numpy as np


train_filename = "tmp/sign_language/sign_mnist_train.csv"
test_filename = "tmp/sign_language/sign_mnist_test.csv"


# This needs to return numpy arrays
def make_dataset(filename):
    labels = []
    features = []
    with open(filename) as source_file:
        csv_reader = csv.reader(source_file, delimiter=",")
        _ = next(csv_reader)

        for row in csv_reader:
            labels.append(row[0])
            features.append(row[1:])

    row_count = len(labels)
    labels = np.array(labels).astype("float32")
    features = np.array(features).astype("float32").reshape((row_count, 28, 28))

    return features, labels


X_train_full, y_train_full = make_dataset(train_filename)
#X_train, X_valid = X_train_full[:24000], X_train_full[24000:]
#y_train, y_valid = y_train_full[:24000], y_train_full[24000:]
X_test, y_test = make_dataset(test_filename)


def plot_image(img):
    img = np.expand_dims(img, axis=-1)
    plt.imshow(img, cmap="Greys_r")
    plt.show()


def make_generator(images, labels):
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1.0/255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        fill_mode="nearest"
    )
    images = np.expand_dims(images, -1)
    generator = datagen.flow(x=images, y=labels, batch_size=32)
    return generator


def make_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(64, (3,3), activation="relu", input_shape=(28,28,1)),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Conv2D(128, (3,3), activation="relu"),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(26, activation="softmax")
    ])
    return model


def plot_history(hist):
    print(hist.history.keys())
    accuracy = hist.history["accuracy"]
    val_accuracy = hist.history["val_accuracy"]
    plt.plot(accuracy, color="b")
    plt.plot(val_accuracy, color="r")
    plt.show()


def test_setup():
    epochs = 15
    gen = make_generator(X_train_full, y_train_full)
    valid_gen = make_generator(X_test, y_test)
    m = make_model()
    m.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    h = m.fit(gen, epochs=epochs, validation_data=valid_gen)
    plot_history(h)
    return h

