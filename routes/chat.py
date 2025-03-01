from flask import Blueprint
from flask_socketio import emit, join_room, leave_room
from app import socketio

chat_bp = Blueprint("chat", __name__)

@socketio.on("connect")
def handle_connect():
    print("A user connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("A user disconnected")

@socketio.on("join")
def handle_join(data):
    room = data["room"]
    join_room(room)
    emit("message", {"message": f"User joined room {room}"}, room=room)

@socketio.on("leave")
def handle_leave(data):
    room = data["room"]
    leave_room(room)
    emit("message", {"message": f"User left room {room}"}, room=room)

@socketio.on("message")
def handle_message(data):
    room = data["room"]
    message = data["message"]
    emit("message", {"message": message}, room=room)