import os
import sys
import psycopg2
from config import config

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_alembic_version():
    # Get database configuration
    config_name = os.environ.get('FLASK_ENV', 'default')
    db_config = config[config_name]
    database_url = db_config.SQLALCHEMY_DATABASE_URI
    
    # Connect to the database
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()
    
    # Check alembic_version table
    try:
        cur.execute("SELECT version_num FROM alembic_version;")
        version = cur.fetchone()
        if version:
            print(f"Alembic version: {version[0]}")
        else:
            print("Alembic version table is empty")
    except Exception as e:
        print(f"Error querying alembic_version table: {e}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    check_alembic_version()