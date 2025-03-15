import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

    # PostgreSQL database on Render
    DATABASE_URI = os.getenv(
        'DATABASE_URI',
        'postgresql://fraud_detection_db_yhyu_user:QpeBJon5SXltjAs2AjkTTARwFzZ1yWFc@dpg-cvap03drie7s7397gd20-a.oregon-postgres.render.com/fraud_detection_db_yhyu'
    )

config = Config()