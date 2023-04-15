import tensorflow as tf
import os
import numpy as np

data_url = "https://drive.google.com/uc?id=15UqmiIm0xwh9mt0IYq2z3jHaauxQSTQT"
filename = "irish-lyrics-eof.txt"

#os.system(f'wget {data_url} -O "irish-lyrics-eof.txt" ')

data = open(filename).read()
corpus = data.lower().split("\n")

tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(corpus)
total_words = len(tokenizer.word_index) + 1 # +1 because of padding token
print(total_words)

input_sequences = []

for line in corpus:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

max_sequence_len = max([len(x) for x in input_sequences])

input_sequences = tf.keras.preprocessing.sequence.pad_sequences(
    input_sequences,
    maxlen=max_sequence_len,
    padding="pre")

xs, labels = input_sequences[:, :-1], input_sequences[:,-1]
ys = tf.keras.utils.to_categorical(labels, num_classes=total_words)

embedding_dim = 100
lstm_units = 150
learning_rate = 0.01

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(total_words, embedding_dim, input_length=max_sequence_len-1),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(lstm_units)),
    tf.keras.layers.Dense(total_words, activation="softmax")
])

model.compile(
    loss="categorical_crossentropy",
    optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
    metrics=['accuracy']
)

epochs = 10
history = model.fit(xs, ys, epochs=epochs)

seed_text = "help me obi-wan kinobi youre my only hope"

# Define total words to predict
next_words = 100

# Define total words to predict

# Loop until desired length is reached
for _ in range(next_words):

    # Convert the seed text to a token sequence
    token_list = tokenizer.texts_to_sequences([seed_text])[0]

    # Pad the sequence
    token_list = tf.keras.preprocessing.sequence.pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')

    # Feed to the model and get the probabilities for each index
    probabilities = model.predict(token_list, verbose=0)

    # Get the index with the highest probability
    predicted = np.argmax(probabilities, axis=-1)[0]

    # Ignore if index is 0 because that is just the padding.
    if predicted != 0:
        # Look up the word associated with the index.
        output_word = tokenizer.index_word[predicted]

        # Combine with the seed text
        seed_text += " " + output_word

# Print the result
print(seed_text)

seed_text = "help me obi-wan kinobi youre my only hope"

# Loop until desired length is reached
for _ in range(next_words):

    # Convert the seed text to a token sequence
    token_list = tokenizer.texts_to_sequences([seed_text])[0]

    # Pad the sequence
    token_list = tf.keras.preprocessing.sequence.pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')

    # Feed to the model and get the probabilities for each index
    probabilities = model.predict(token_list, verbose=0)

    # Pick a random number from [1,2,3]
    choice = np.random.choice([1, 2, 3])

    # Sort the probabilities in ascending order
    # and get the random choice from the end of the array
    predicted = np.argsort(probabilities)[0][-choice]

    # Ignore if index is 0 because that is just the padding.
    if predicted != 0:
        # Look up the word associated with the index.
        output_word = tokenizer.index_word[predicted]

        # Combine with the seed text
        seed_text += " " + output_word

# Print the result
print(seed_text)
