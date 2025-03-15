from flask import Blueprint, request, jsonify
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