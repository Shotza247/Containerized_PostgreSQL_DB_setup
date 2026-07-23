import psycopg2
import logging as log
import os
#from dotenv import load_dotenv

#load_dotenv()  # Load environment variables from .env file

try:
    # 1. Connect to the PostgreSQL database running in Docker
    DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}
    
    connection = psycopg2.connect(**DB_CONFIG)

    # 2. Create a cursor object to execute SQL commands
    cursor = connection.cursor()
    
    # 3. Print PostgreSQL version to confirm connection success
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"✅ Successfully connected! Database version: {db_version[0]}")

    # 4. (Optional) Create a test table and insert a row
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL
        );
    """)
    
    cursor.execute("INSERT INTO test_users (name) VALUES ('Alice') RETURNING id;")
    user_id = cursor.fetchone()[0]
    print(f"📝 Inserted test user with ID: {user_id}")
    
    # Commit changes to the database
    connection.commit()

except Exception as error:
    print(f"❌ Error connecting to PostgreSQL: {error}")

finally:
    # 5. Clean up and close connections
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
        print("🔒 PostgreSQL connection closed.")
