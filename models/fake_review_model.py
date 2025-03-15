import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Ensure that the "models" directory exists
os.makedirs('models', exist_ok=True)

# Load dataset
reviews = ["This product is great!", "Worst experience ever", "Amazing!"]
labels = [1, 0, 1]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(reviews)

model = MultinomialNB()
model.fit(X, labels)

# Save the model in the "models" directory
with open('models/fake_review_model.pkl', 'wb') as f:
    pickle.dump((vectorizer, model), f)

print("✅ Model saved successfully in 'models/fake_review_model.pkl'")