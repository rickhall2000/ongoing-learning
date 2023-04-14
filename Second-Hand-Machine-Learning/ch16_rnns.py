import tensorflow as tf

filename = "shakespeare.txt"
shakespeare_url = "https://homl.info/shakespeare"
fullpath = "/Users/richardhall/.keras/datasets/shakespeare.txt"

def download_data():
    filepath = tf.keras.utils.get_file(filename, shakespeare_url)


def read_data():
    with open(fullpath) as f:
        shakespeare_text = f.read()
    return shakespeare_text

