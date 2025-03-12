from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "student_login"

# Import routes
from routes.student import student_bp
from routes.admin import admin_bp
from routes.quiz import quiz_bp

app.register_blueprint(student_bp, url_prefix="/student")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(quiz_bp, url_prefix="/quiz")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
