from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from app.config import Config
import os
#from app.models import User
app = Flask(__name__)
db = SQLAlchemy()
#login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail(app)
migrate = Migrate()

login_manager = LoginManager(app)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["UPLOAD_FOLDER"]="app/static/images"
    if not os.path.exists('app/static/images'):
        os.makedirs('app/static/images')
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from app.routes import main
    app.register_blueprint(main)
    
    return app
    




