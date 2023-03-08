import os
import zipfile
import random
import shutil
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Paths
source_path = 'tmp/PetImages'
root_dir = "tmp/cats-v-dogs"
source_path_dogs = os.path.join(source_path, 'Dog')
source_path_cats = os.path.join(source_path, 'Cat')
train_path = os.path.join(root_dir, "training")
valid_path = os.path.join(root_dir, "validation")
cat_train_dir = os.path.join(train_path, "Cat")
dog_train_dir = os.path.join(train_path, "Dog")
dog_valid_dir = os.path.join(valid_path, "Dog")
cat_valid_dir = os.path.join(valid_path, "Cat")
split_size = 0.9


def load_files():
    os.system (
        'wget --no-check-certificate \
            "https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_5340.zip" \
            -O "tmp/cats-and-dogs.zip"' )

    local_zip = 'tmp/cats-and-dogs.zip'
    zip_ref   = zipfile.ZipFile(local_zip, 'r')
    zip_ref.extractall('tmp')
    zip_ref.close()

    os.system('find tmp/PetImages/ -type f ! -name "*.jpg" -exec rm {} +')

    if os.path.exists(root_dir):
        shutil.rmtree(root_dir)

    create_train_val_dirs()

def create_train_val_dirs():
    os.makedirs(train_path)
    os.makedirs(valid_path)
    os.makedirs(cat_train_dir)
    os.makedirs(cat_valid_dir)
    os.makedirs(dog_train_dir)
    os.makedirs(dog_valid_dir)

def reload_test():
    print("Reload load")

def split_data(source_dir, training_dir, validation_dir, split_size):
    files = os.listdir(source_dir)
    file_list = []
    for f in files:
        full_name = os.path.join(source_dir, f)
        if os.path.getsize(full_name) > 0:
            file_list.append(f)

    file_count = len(file_list)
    split_count = int(file_count * split_size)
    print(file_count, split_count)
    random_list = random.sample(file_list, file_count)
    training_files = random_list[:split_count]
    validation_files = random_list[split_count:]

    for f in training_files:
        source_file = os.path.join(source_dir, f)
        dest_file = os.path.join(training_dir, f)
        shutil.copyfile(source_file, dest_file)

    for f in validation_files:
        source_file = os.path.join(source_dir, f)
        dest_file = os.path.join(validation_dir, f)
        shutil.copyfile(source_file, dest_file)

def train_val_generators(TRAINING_DIR, VALIDATION_DIR):
    train_datagen = ImageDataGenerator(rescale=1.0/255.)
    train_generator = train_datagen.flow_from_directory(directory=TRAINING_DIR,
                                                        batch_size=20,
                                                        class_mode="binary",
                                                        target_size=(150, 150))

    valid_datagen = ImageDataGenerator(rescale=1.0/255.)
    valid_generator = valid_datagen.flow_from_directory(directory=VALIDATION_DIR,
                                                        batch_size=20,
                                                        class_mode="binary",
                                                        target_size=(150, 150))

    return train_generator, valid_generator

def show_images():
    pic_index = 0
    nrows = 4
    ncols = 4
    fig = plt.gcf()
    fig.set_size_inches(ncols * 4, nrows * 4)

    pic_index += 8
    train_cat_fnames = os.listdir(cat_train_dir)
    train_dog_fnames = os.listdir(dog_train_dir)

    next_cat_pix = [os.path.join(cat_train_dir, fname)
                    for fname in train_cat_fnames[pic_index - 4:pic_index]
                    ]

    next_dog_pix = [os.path.join(dog_train_dir, fname)
                    for fname in train_dog_fnames[pic_index - 4:pic_index]
                    ]

    for i, img_path in enumerate(next_cat_pix + next_dog_pix):
        # Set up subplot; subplot indices start at 1
        sp = plt.subplot(nrows, ncols, i + 1)
        sp.axis('Off')  # Don't show axes (or gridlines)

        img = mpimg.imread(img_path)
        plt.imshow(img)

    plt.show()

def create_model():
    # create and compile the model
    # 3 conv layers
    # end with a binary layr
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(16, (3, 3), activation="relu", input_shape=(150, 150, 3)),
        tf.keras.layers.MaxPool2D(2,2),
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
        tf.keras.layers.MaxPool2D(2,2),
        tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
        tf.keras.layers.MaxPool2D(2,2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])

    model.compile(optimizer="Adam",
                  loss="binary_crossentropy",
                  metrics=["accuracy"])

    return model

def train_model():
    train_generator, validation_generator = train_val_generators(train_path, valid_path)

    model = create_model()
    history = model.fit(train_generator,
                        epochs=15,
                        verbose=1,
                        validation_data=validation_generator)
    return history


#show_images()

history = train_model()

acc=history.history['accuracy']
val_acc=history.history['val_accuracy']
loss=history.history['loss']
val_loss=history.history['val_loss']
print("Here I am")

epochs=range(len(acc)) # Get number of epochs

#------------------------------------------------
# Plot training and validation accuracy per epoch
#------------------------------------------------
plt.plot(epochs, acc, 'r', "Training Accuracy")
plt.plot(epochs, val_acc, 'b', "Validation Accuracy")
plt.title('Training and validation accuracy')
plt.show()
print("")

#------------------------------------------------
# Plot training and validation loss per epoch
#------------------------------------------------
plt.plot(epochs, loss, 'r', "Training Loss")
plt.plot(epochs, val_loss, 'b', "Validation Loss")
plt.show()