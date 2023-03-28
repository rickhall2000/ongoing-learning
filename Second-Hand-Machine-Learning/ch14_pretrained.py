import tensorflow as tf
from sklearn.datasets import load_sample_images
import tensorflow_datasets as tfds

def sample_resnet():
    model = tf.keras.applications.ResNet50(weights="imagenet")

    images = load_sample_images()["images"]
    images_resized = tf.keras.layers.Resizing(height=224, width=224,
                                              crop_to_aspect_ratio=True)(images)

    inputs = tf.keras.applications.resnet50.preprocess_input(images_resized)

    Y_proba = model.predict(inputs)
    top_K = tf.keras.applications.resnet50.decode_predictions(Y_proba, top=3)
    for image_index in range(len(images)):
        print(f"Image #{image_index}")
        for class_id, name, y_proba in top_K[image_index]:
            print(f" {class_id} - {name:12s} {y_proba:.2%}")
    return Y_proba

def transfer_learning():
    dataset, info = tfds.load("tf_flowers", as_supervised=True, with_info=True)
    dataset_size = info.splits["train"].num_examples
    class_names = info.features["label"].names
    n_classes = info.features["label"].num_classes

    test_set_raw, valid_set_raw, train_set_raw = tfds.load(
        "tf_flowers",
        split=["train[:10%]", "train[10%:25%]", "train[25%:]"],
        as_supervised=True
    )

    batch_size = 32
    preprocess = tf.keras.Sequential([
        tf.keras.layers.Resizing(height=224, width=224, crop_to_aspect_ratio=True),
        tf.keras.layers.Lambda(tf.keras.applications.xception.preprocess_input)
    ])
    train_set = train_set_raw.map(lambda X, y: (preprocess(X), y))
    train_set = train_set.shuffle(1000, seed=42).batch(batch_size).prefetch(1)
    valid_set = valid_set_raw.map(lambda X, y: (preprocess(X), y)).batch(batch_size)
    test_set = test_set_raw.map(lambda X, y: (preprocess(X), y)).batch(batch_size)

    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip(mode="horizontal", seed=42),
        tf.keras.layers.RandomRotation(factor=0.05, seed=42),
        tf.keras.layers.RandomContrast(factor=0.2, seed=42)
    ])

    base_model = tf.keras.applications.xception.Xception(weights="imagenet",
                                                         include_top=False)
    avg = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
    output = tf.keras.layers.Dense(n_classes, activation="softmax")(avg)
    model = tf.keras.Model(inputs=base_model.input, outputs=output)

    for layer in base_model.layers:
        layer.trainable=False

    optimizer = tf.keras.optimizers.SGD(learning_rate=0.1, momentum=0.9)
    model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer,
                  metrics=["accuracy"])
    history = model.fit(train_set, validation_data=valid_set, epochs=3)

    # top layer is trained, now let's fine tune a bit
    for layer in base_model.layers[56:]:
        layer.trainable = True

    optimizer = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9)
    model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer,
                   metrics=["accuracy"])
    history = model.fit(train_set, validation_data=valid_set, epochs=10)

    return history
