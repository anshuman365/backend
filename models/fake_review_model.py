import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Sample dataset
reviews = ["This product is great!", "Worst experience ever", "Amazing!", "Not worth the price", "Highly recommended"]
labels = np.array([1, 0, 1, 0, 1])  # 1 = Real, 0 = Fake

# Tokenize and pad sequences
tokenizer = Tokenizer(num_words=1000, oov_token="<OOV>")
tokenizer.fit_on_texts(reviews)
X = tokenizer.texts_to_sequences(reviews)
X = pad_sequences(X, maxlen=10)

# Define LSTM Model
model = Sequential([
    Embedding(input_dim=1000, output_dim=64, input_length=10),
    LSTM(64, return_sequences=True),
    GlobalAveragePooling1D(),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, labels, epochs=10, verbose=1)

# Save model and tokenizer
model.save('fake_review_model.h5')
with open('tokenizer.pkl', 'wb') as f:
    pickle.dump(tokenizer, f) 