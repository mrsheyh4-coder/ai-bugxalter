import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    if not postgres_password:
        raise RuntimeError("POSTGRES_PASSWORD environment variable is required")

    # Connect to the default 'postgres' database
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password=postgres_password,
        host='localhost'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    # Check if database exists
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'ai_buxgalter'")
    exists = cur.fetchone()
    
    if not exists:
        print("Creating database 'ai_buxgalter'...")
        cur.execute('CREATE DATABASE ai_buxgalter')
        print("Database created successfully.")
    else:
        print("Database 'ai_buxgalter' already exists.")
        
    cur.close()
    conn.close()

if __name__ == "__main__":
    try:
        create_database()
    except Exception as e:
        print(f"Error creating database: {e}")
