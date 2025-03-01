from flask import Blueprint, request, jsonify
from database import db
from models.user import User

match_bp = Blueprint("match", __name__)

@match_bp.route("/set_frequency", methods=["POST"])
def set_frequency():
    data = request.json
    user_id = data.get("user_id")
    frequency = data.get("frequency")

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.frequency = frequency
    db.session.commit()
    return jsonify({"message": "Frequency updated"}), 200

@match_bp.route("/find_match/<int:user_id>", methods=["GET"])
def find_match(user_id):
    user = User.query.get(user_id)
    if not user or user.frequency is None:
        return jsonify({"error": "User not found or frequency not set"}), 404

    matched_user = User.query.filter(User.id != user_id, User.frequency == user.frequency).first()

    if matched_user:
        return jsonify({"match": matched_user.username, "match_id": matched_user.id}), 200
    return jsonify({"message": "No match found"}), 200