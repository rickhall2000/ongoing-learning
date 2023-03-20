import os
import zipfile
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def download_model():
    # notop means that it oes not contain the top layers
    os.system("wget --no-check-certificate \
        https://storage.googleapis.com/mledu-datasets/inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5 \
        -O tmp/inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5")

def read_model():
    local_weights_file = "tmp/inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5"

    pretrained_model = InceptionV3(input_shape = (150,150, 3),
                                   include_top = False,
                                   weights=None)
    pretrained_model.load_weights(local_weights_file)
    for layer in pretrained_model.layers:
        layer.trainable = False

    return pretrained_model

start_model = read_model()

def add_training_layers(model):
    last_layer = model.get_layer('mixed7')
    last_output = last_layer.output
    x = layers.Flatten()(last_output)
    x = layers.Dense(1024, activation="relu")(x)
    x = layers.Dropout(0.2)(x)
    x = layers.Dense(1, activation="sigmoid")(x)
    model = tf.keras.Model(model.input, x)
    model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.0001),
                  loss="binary_crossentropy",
                  metrics = ['accuracy'])
    return model

def download_data():
    os.system("wget https://storage.googleapis.com/tensorflow-1-public/course2/cats_and_dogs_filtered.zip")


base_dir = 'tmp/cats_and_dogs_filtered'
train_dir = os.path.join( base_dir, 'train')
validation_dir = os.path.join( base_dir, 'validation')
train_cats_dir = os.path.join(train_dir, 'cats')
train_dogs_dir = os.path.join(train_dir, 'dogs')
validation_cats_dir = os.path.join(validation_dir, 'cats')
validation_dogs_dir = os.path.join(validation_dir, 'dogs')


def extract_data():
    zip_ref = zipfile.ZipFile("./cats_and_dogs_filtered.zip", 'r')
    zip_ref.extractall("tmp/")
    zip_ref.close()


def build_generators():
    train_gen = ImageDataGenerator(
        rescale=1.0/255.,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )
    train_data = train_gen.flow_from_directory(train_dir,
                                               class_mode="binary",
                                               target_size=(150,150),
                                               batch_size=20)

    valid_gen = ImageDataGenerator(
        rescale=1.0/255.
    )
    valid_data = valid_gen.flow_from_directory(validation_dir,
                                               class_mode="binary",
                                               target_size=(150,150),
                                               batch_size=20)
    return train_data, valid_data


model = add_training_layers(start_model)
train, test = build_generators()

history = model.fit(
    train,
    validation_data=test,
    steps_per_epoch=100,
    epochs=20,
    validation_steps=50,
    verbose=1)


import matplotlib.pyplot as plt
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend(loc=0)

plt.show()