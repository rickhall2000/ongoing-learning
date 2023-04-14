import json
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

#os.system("wget https://storage.googleapis.com/tensorflow-1-public/course3/sarcasm.json")
training_size = 20000
vocab_size = 10000
max_length = 32
embedding_dim = 16
oov_token="<OOV>"

# load the data
sentences = []
labels = []
with open("sarcasm.json") as f:
    datastore = json.load(f)

for item in datastore:
    sentences.append(item['headline'])
    labels.append(item['is_sarcastic'])

# split the data
train_sentences, test_sentences = sentences[:training_size], sentences[training_size:]
train_labels, test_labels = labels[:training_size], labels[training_size:]

tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(train_sentences)
word_index = tokenizer.word_index

train_sequences = tokenizer.texts_to_sequences(train_sentences)
train_padded = tf.keras.preprocessing.sequence.pad_sequences(train_sequences,
                                                             max_length,
                                                             padding="post",
                                                             truncating="post")

test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = tf.keras.preprocessing.sequence.pad_sequences(test_sequences,
                                                            max_length,
                                                            padding="post",
                                                            truncating="post")

train_labels = np.array(train_labels)
test_labels = np.array(test_labels)


model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
#    tf.keras.layers.Conv1D(128, 5, activation="relu"),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
#    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dropout(.4),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dropout(.4),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

early_stopping_cb = tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True, monitor="val_accuracy")

history = model.fit(train_padded,
                    train_labels,
                    validation_data=(test_padded, test_labels),
                    epochs=30,
                    callbacks=[early_stopping_cb])

accuracy = history.history["accuracy"]
val_accuracy = history.history["val_accuracy"]

plt.plot(accuracy, color="b")
plt.plot(val_accuracy, color="r")
plt.show()
