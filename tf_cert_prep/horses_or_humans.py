# I am going to build a model that trains the images
# I am going to plot the accuracy of the model, and the validation accuracy

import os
import zipfile
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tensorflow as tf

train_url = "https://storage.googleapis.com/tensorflow-1-public/course2/week3/horse-or-human.zip"
test_url = "https://storage.googleapis.com/tensorflow-1-public/course2/week3/validation-horse-or-human.zip"

train_horse_dir = os.path.join('tmp/horse-or-human/horses')
train_human_dir = os.path.join('tmp/horse-or-human/humans')
validation_horse_dir = os.path.join('tmp/validation-horse-or-human/horses')
validation_human_dir = os.path.join('tmp/validation-horse-or-human/humans')

target_accuracy = 0.9
target_val_accuracy = 0.85

class MyCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        acc = logs.get("accuracy")
        val_acc = logs.get("val_accuracy")
        if acc > target_accuracy and val_acc > target_val_accuracy:
            self.model.stop_training = True

def download_the_images():
    os.system(f"wget {train_url}")
    os.system(f"wget {test_url}")

    zip_ref = zipfile.ZipFile('./horse-or-human.zip', 'r')
    zip_ref.extractall('tmp/horse-or-human')

    zip_ref = zipfile.ZipFile('./validation-horse-or-human.zip', 'r')
    zip_ref.extractall('tmp/validation-horse-or-human')

    zip_ref.close()


def show_an_image():
    horse = os.listdir(train_horse_dir)[0]
    horse = os.path.join(train_horse_dir, horse)

    plt.gcf()
    img = mpimg.imread(horse)
    plt.imshow(img)
    plt.show()

def make_img_generators():
    train_img_gen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1.0/255.,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        fill_mode="nearest",
        horizontal_flip=True,
        vertical_flip=True
    )
    test_img_gen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1.0/255.
    )

    train_gen = train_img_gen.flow_from_directory('tmp/horse-or-human',
                                      target_size=(300,300),
                                      batch_size=128,
                                      class_mode="binary")

    test_gen = test_img_gen.flow_from_directory('tmp/validation-horse-or-human',
                                     target_size=(300, 300),
                                     batch_size=32,
                                     class_mode="binary")

    return train_gen, test_gen

def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(16, kernel_size=(3,3), activation="relu", input_shape=(300,300,3)),
        tf.keras.layers.MaxPool2D(2,2),
        tf.keras.layers.Conv2D(32, kernel_size=(3,3), activation="relu"),
        tf.keras.layers.MaxPool2D(2,2),
        tf.keras.layers.Conv2D(64, kernel_size=(3,3), activation="relu"),
        tf.keras.layers.MaxPool2D(2,2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])

    model.compile(optimizer="Adam", loss="binary_crossentropy", metrics=["accuracy"])

    return model

def do_training():
    EPOCHS = 50
    STEPS = 8
    train_img_gen, test_img_gen = make_img_generators()
    model = build_model()
    hist = model.fit(train_img_gen,
                     steps_per_epoch=STEPS,
                     epochs=EPOCHS,
                     verbose=1,
                     validation_data=test_img_gen,
                     validation_steps=8,
                     callbacks=[MyCallback()])
    return hist

def plot_progress(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    epochs = range(len(acc))

    plt.plot(epochs, acc, 'r', label="Training accuracy")
    plt.plot(epochs, val_acc, 'b', label="Validation accuracy")
    plt.title("Training and validation accuracy")

    plt.show()


history = do_training()
plot_progress(history)