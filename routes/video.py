from flask import Blueprint, request, jsonify
from flask_socketio import emit
from app import socketio

video_bp = Blueprint("video", __name__)

@socketio.on("offer")
def handle_offer(data):
    receiver_id = data["receiver_id"]
    emit("offer", data, room=receiver_id)

@socketio.on("answer")
def handle_answer(data):
    sender_id = data["sender_id"]
    emit("answer", data, room=sender_id)

@socketio.on("ice-candidate")
def handle_ice_candidate(data):
    recipient_id = data["recipient_id"]
    emit("ice-candidate", data, room=recipient_id)