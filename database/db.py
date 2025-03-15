import psycopg2
from config import config

try:
    conn = psycopg2.connect(config.DATABASE_URI)
    cursor = conn.cursor()
    print("✅ Successfully connected to PostgreSQL Database!")

except Exception as e:
    print(f"❌ Database Connection Failed: {e}")