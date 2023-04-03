from PIL import Image
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

train_dir = "wildcats/train"
test_dir = "wildcats/test"
valid_dir = "wildcats/valid"


def sample_image():
    lion_dir = os.path.join(train_dir, "LIONS")
    first_lion = os.listdir(lion_dir)[0]
    lion_im = Image.open(os.path.join(lion_dir, first_lion))
    print(lion_im.format, lion_im.size, lion_im.mode)
    lion_im.show()


def find_image_sizes(rootpath):
    file_sizes = {}
    for sub_dir in os.listdir(rootpath):
        sub_path = os.path.join(rootpath, sub_dir)
        for filename in os.listdir(sub_path):
            fullname = os.path.join(sub_path, filename)
            im_size = Image.open(fullname).size
            current_count = file_sizes.get(im_size, 0)
            file_sizes[im_size] = current_count + 1
    return file_sizes


def build_image_generators():
    train_gen = ImageDataGenerator(rescale=1./255,
                                   horizontal_flip=True,
                                   rotation_range=20,
                                   shear_range=0.1,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2)
    train_data = train_gen.flow_from_directory(train_dir, target_size=(224,224), class_mode="categorical")
    valid_gen = ImageDataGenerator(rescale=1./255)
    valid_data = valid_gen.flow_from_directory(valid_dir, target_size=(224, 224), class_mode="categorical")
    test_gen = ImageDataGenerator(rescale=1./255)
    test_data = test_gen.flow_from_directory(test_dir, target_size=(224,224), class_mode="categorical")
    return train_data, valid_data, test_data


def build_model():
    padding = "same"
    initializer= "he_normal"
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, kernel_size=(3,3), activation="relu",
                               padding=padding, kernel_initializer=initializer),
        tf.keras.layers.Conv2D(32, kernel_size=(3,3), activation="relu",
                               padding=padding, kernel_initializer=initializer),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
        tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation="relu",
                               padding=padding, kernel_initializer=initializer),
        tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation="relu",
                               padding=padding, kernel_initializer=initializer),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(10, activation="softmax")
    ])
    return model


def compile_model(model):
    optimizer = tf.keras.optimizers.Adam()
    model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])
    return model


def train_model(model, train_data, valid_data, epochs=10):
    stop_early = tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)
    history = model.fit(train_data, epochs=epochs, validation_data=valid_data, callbacks=[stop_early])
    return history


def plot_history(history):
    accuracy = history.history["accuracy"]
    val_accuracy = history.history["val_accuracy"]
    plt.plot(accuracy, color="blue")
    plt.plot(val_accuracy, color="red")
    plt.show()


def do_the_thing():
    train, valid, test = build_image_generators()
    m = build_model()
    m = compile_model(m)
    h = train_model(m, train, valid, 50)
    plot_history(h)
    return m, h


def get_inception():
    base_model = tf.keras.applications.inception_v3.InceptionV3(
        include_top=False,
        input_shape=(224, 224, 3))
    return base_model


def transfer_learning():
    base_model = get_inception()

    for layer in base_model.layers:
        layer.trainable = False

    last_layer = base_model.layers[-1]
    last_output = last_layer.output

    Z = tf.keras.layers.Flatten()(last_output)
    Z = tf.keras.layers.Dense(48, activation="relu")(Z)
    Z = tf.keras.layers.Dense(10, activation="softmax")(Z)

    model = tf.keras.Model(base_model.input, Z)

    model.compile(loss="categorical_crossentropy", optimizer="Adam", metrics=["accuracy"])

    train_gen, valid_gen, test_gen = build_image_generators()
    history = model.fit(train_gen, validation_data=valid_gen, epochs=5)

    return history

