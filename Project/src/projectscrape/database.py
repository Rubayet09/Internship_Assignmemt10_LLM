from sqlalchemy import create_engine, text
import os
import time
from sqlalchemy.exc import OperationalError

# Get database URL from environment variable, with a fallback default value
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://myuser:ulala@localhost:5432/tripcom_db')

def get_db_connection():
    """Create database connection with retry logic"""
    max_retries = 5
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            # Create the engine and connect
            engine = create_engine(DATABASE_URL)
            connection = engine.connect()
            print("Connected successfully!")
            return connection
        except OperationalError as e:
            if attempt == max_retries - 1:
                print(f"Failed to connect to database after {max_retries} attempts")
                raise
            print(f"Database connection attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

def query_properties():
    """Query all properties from the database"""
    connection = get_db_connection()
    try:
        # Query to fetch all entries from the properties table
        result = connection.execute(text("SELECT * FROM properties;"))
        
        # Fetch and print all rows from the table
        properties = result.fetchall()
        for row in properties:
            print(row)
    finally:
        # Always close the connection
        connection.close()

if __name__ == "__main__":
    query_properties()
