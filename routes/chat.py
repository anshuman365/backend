from flask import Blueprint, request
from flask_socketio import emit, join_room
from database import db
from models.chat import Chat
from app import socketio  # Import socketio only after initialization

chat_bp = Blueprint("chat", __name__)

@socketio.on("join")
def handle_join(data):
    room = data["room"]
    join_room(room)
    emit("message", {"message": f"User joined {room}"}, room=room)

@socketio.on("message")
def handle_message(data):
    sender_id = data["sender_id"]
    receiver_id = data["receiver_id"]
    msg = data["message"]
    
    # Store message in database
    chat_message = Chat(sender_id=sender_id, receiver_id=receiver_id, message=msg)
    db.session.add(chat_message)
    db.session.commit()
    
    # Send message to chat room
    room = f"{sender_id}_{receiver_id}"  # Unique room for sender-receiver pair
    emit("message", {"message": msg, "sender_id": sender_id}, room=room)