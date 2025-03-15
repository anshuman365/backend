from flask_bcrypt import Bcrypt
from config import config
import psycopg2

bcrypt = Bcrypt()
conn = psycopg2.connect(config.DATABASE_URI)
cursor = conn.cursor()

def create_admin(username, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    cursor.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()