from flask import Blueprint, request, jsonify
from models.scam_detection import detect_scam

scam_api = Blueprint('scam_api', __name__)

@scam_api.route('/detect_scam', methods=['POST'])
def detect_scam_api():
    data = request.json
    description = data.get('description', '')

    result = detect_scam(description)

    return jsonify({'scam': result})