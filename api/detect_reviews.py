from flask import Blueprint, request, jsonify
import os
import pickle

review_api = Blueprint('review_api', __name__)

with open('../models/fake_review_model.pkl', 'rb') as f:
    vectorizer, model = pickle.load(f)

@review_api.route('/detect_review', methods=['POST'])
def detect_fake_review():
    data = request.json
    review_text = data.get('review', '')

    vectorized_text = vectorizer.transform([review_text])
    prediction = model.predict(vectorized_text)

    return jsonify({'fake_review': bool(prediction[0] == 0)})
    

# Get absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '../models/fake_review_model.pkl')

# Load Model
try:
    with open(MODEL_PATH, 'rb') as f:
        vectorizer, model = pickle.load(f)
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print(f"❌ Model file not found at: {MODEL_PATH}")