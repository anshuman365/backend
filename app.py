import eventlet
eventlet.monkey_patch()  # Apply monkey patching before importing anything

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from config import Config
from database import db

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize Database
db.init_app(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Import Routes AFTER initializing `socketio`
from routes.auth import auth_bp
from routes.chat import chat_bp
from routes.match import match_bp

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(chat_bp, url_prefix="/chat")
app.register_blueprint(match_bp, url_prefix="/match")

# Create Database Tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)