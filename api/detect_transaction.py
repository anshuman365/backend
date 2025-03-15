from flask import Blueprint, request, jsonify
import pickle
import numpy as np

transaction_api = Blueprint('transaction_api', __name__)

with open('../models/fraud_transaction_model.pkl', 'rb') as f:
    model = pickle.load(f)

@transaction_api.route('/detect_transaction', methods=['POST'])
def detect_fraud_transaction():
    data = request.json
    amount = float(data.get('amount', 0))

    prediction = model.predict(np.array([[amount]]))

    return jsonify({'fraud': bool(prediction[0] == -1)})