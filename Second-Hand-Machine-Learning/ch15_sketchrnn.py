import tensorflow as tf
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def download_file():
    tf_download_root = "http://download.tensorflow.org/data/"
    filename = "quickdraw_tutorial_dataset_v1.tar.gz"
    filepath = tf.keras.utils.get_file(filename,
                                       tf_download_root + filename,
                                       cache_dir=".",
                                       extract=True)
    print(filepath)
    return filepath

def get_filenames():
    filepath = './datasets/quickdraw_tutorial_dataset_v1.tar.gz'
    quickdraw_dir = Path(filepath).parent
    train_files = sorted(
        [str(path) for path in quickdraw_dir.glob("training.tfrecord-*")]
    )
    eval_files = sorted(
        [str(path) for path in quickdraw_dir.glob("eval.tfrecord-*")]
    )

    with open(quickdraw_dir / "eval.tfrecord.classes") as test_classes_file:
        test_classes = test_classes_file.readlines()

    with open(quickdraw_dir / "training.tfrecord.classes") as train_classes_file:
        train_classes = train_classes_file.readlines()

    class_names = [name.strip().lower() for name in train_classes]
    return train_files, eval_files, class_names


def parse(data_batch):
    feature_descriptions = {
        "ink": tf.io.VarLenFeature(dtype=tf.float32),
        "shape": tf.io.FixedLenFeature([2], dtype=tf.int64),
        "class_index": tf.io.FixedLenFeature([1], dtype=tf.int64)
    }
    examples = tf.io.parse_example(data_batch, feature_descriptions)
    flat_sketches = tf.sparse.to_dense(examples["ink"])
    sketches = tf.reshape(flat_sketches, shape=[tf.size(data_batch), -1, 3])
    lengths = examples["shape"][:, 0]
    labels = examples["class_index"][:, 0]
    return sketches, lengths, labels


def quickdraw_dataset(filepaths, batch_size=32, shuffle_buffer_size=None,
                      n_parse_threads=5, n_read_threads=5, cache=False):
    dataset = tf.data.TFRecordDataset(filepaths,
                                      num_parallel_reads=n_read_threads)
    if cache:
        dataset = dataset.cache()
    if shuffle_buffer_size:
        dataset = dataset.shuffle(shuffle_buffer_size)
    dataset = dataset.batch(batch_size)
    dataset = dataset.map(parse, num_parallel_calls=n_parse_threads)
    return dataset.prefetch(1)


train_files, eval_files, class_names = get_filenames()

train_set = quickdraw_dataset(train_files, shuffle_buffer_size=10000)
valid_set = quickdraw_dataset(eval_files[:5])
test_set = quickdraw_dataset(eval_files[5:])


def draw_sketch(sketch, label=None):
    origin = np.array([[0., 0., 0.]])
    sketch = np.r_[origin, sketch]
    stroke_end_indices = np.argwhere(sketch[:, -1]==1.)[:, 0]
    coordinates = sketch[:, :2].cumsum(axis=0)
    strokes = np.split(coordinates, stroke_end_indices + 1)
    title = class_names[label.numpy()] if label is not None else "Try to guess"
    plt.title(title)
    plt.plot(coordinates[:, 0], -coordinates[:, 1], "y:")
    for stroke in strokes:
        plt.plot(stroke[:, 0], -stroke[:, 1], ".-")
    plt.axis("off")


def draw_sketches(sketches, lengths, labels):
    n_sketches = len(sketches)
    n_cols = 4
    n_rows = (n_sketches - 1) // n_cols + 1
    plt.figure(figsize=(n_cols * 3, n_rows * 3.5))
    for index, sketch, length, label in zip(range(n_sketches), sketches, lengths, labels):
        plt.subplot(n_rows, n_cols, index + 1)
        draw_sketch(sketch[:length], label)
    plt.show()


def show_drawings(train_set):
    for sketches, lengths, labels in train_set.take(1):
        draw_sketches(sketches, lengths, labels)

def crop_long_sketches(dataset, max_length=100):
    return dataset.map(lambda inks, lengths, labels: (inks[:, :max_length], labels))

cropped_train_set = crop_long_sketches(train_set)
cropped_valid_set = crop_long_sketches(valid_set)
cropped_test_set = crop_long_sketches(test_set)


def build_model():
    tf.keras.backend.clear_session()
    model = tf.keras.Sequential([
        tf.keras.layers.Conv1D(32, kernel_size=5, strides=2, activation="relu"),
        tf.keras.layers.Conv1D(64, kernel_size=5, strides=2, activation="relu"),
        tf.keras.layers.LSTM(64, return_sequences=True),
        tf.keras.layers.LSTM(64),
        tf.keras.layers.Dense(len(class_names), activation="softmax")
    ])
    optimizer = tf.keras.optimizers.SGD(learning_rate=.002, clipnorm=1.)
    model.compile(optimizer=optimizer, loss="sparse_categorical_crossentropy",
                  metrics=["accuracy", "sparse_top_k_categorical_accuracy"])
    return model

def train_model(model):
    history = model.fit(cropped_train_set, epochs=2, validation_data=cropped_valid_set)
    return history


def run_the_thing():
    m = build_model()
    h = train_model(m)
    return h