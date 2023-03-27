from sklearn.datasets import load_sample_images
import tensorflow as tf


images = load_sample_images()["images"]
images = tf.keras.layers.CenterCrop(height=70, width=120)(images)
images = tf.keras.layers.Rescaling(scale=1 / 255)(images)

conv_layer = tf.keras.layers.Conv2D(filters=32, kernel_size=7)
fmaps = conv_layer(images)

max_pool = tf.keras.layers.MaxPool2D(pool_size=2)
pooled = max_pool(fmaps)

global_avg_pool = tf.keras.layers.GlobalAvgPool2D()
global_pooled = global_avg_pool(fmaps)

global_avg_pool_alt = tf.keras.layers.Lambda(
    lambda X: tf.reduce_mean(X, axis=[1,2])
)

avg_img = global_avg_pool_alt(images)


class DepthPool(tf.keras.layers.Layer):
    def __init__(self, pool_size=2, **kwargs):
        super().__init__(**kwargs)
        self.pool_size = pool_size

    def call(self, inputs):
        shape = tf.shape(inputs)
        groups = shape[-1]
        new_shape = tf.concat([shape[:-1], [groups, self.pool_size]], axis=0)
        return tf.reduce_max(tf.reshape(inputs, new_shape), axis=-1)
