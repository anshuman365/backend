import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = "postgresql://e_commerce_database_83mb_user:w3ApiBl9lcavvc17VpmAh7ykgIdwod0a@dpg-cva14gpc1ekc738orhn0-a/e_commerce_database_83mb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_TIMEOUT = 30
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = "raghuvanshirohit777@gmail.com"
    SECURITY_PASSWORD_SALT = os.urandom(16).hex()
    
