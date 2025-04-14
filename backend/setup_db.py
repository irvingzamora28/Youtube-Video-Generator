"""
Simple database setup script.
"""
import os
import sqlite3
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = SCRIPT_DIR / "database"
DB_FILE = DB_DIR / "vidgen.db"
SCHEMA_FILE = DB_DIR / "schema.sql"
STORAGE_DIR = SCRIPT_DIR / "storage"

def setup_database():
    """Set up the database and storage directories."""
    # Create database directory
    os.makedirs(DB_DIR, exist_ok=True)
    
    # Read schema file
    try:
        with open(SCHEMA_FILE, 'r') as f:
            schema = f.read()
    except FileNotFoundError:
        logger.error(f"Schema file not found at {SCHEMA_FILE}")
        return False
    
    # Create and initialize database
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.executescript(schema)
        conn.commit()
        
        # Check tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        logger.info(f"Database initialized at {DB_FILE}")
        logger.info("Tables created:")
        for table in tables:
            logger.info(f"- {table[0]}")
        
        conn.close()
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        return False
    
    # Create storage directories
    try:
        # Main storage directory
        os.makedirs(STORAGE_DIR, exist_ok=True)
        
        # Projects directory
        projects_dir = STORAGE_DIR / "projects"
        os.makedirs(projects_dir, exist_ok=True)
        
        logger.info(f"Storage directories initialized at {STORAGE_DIR}")
    except Exception as e:
        logger.error(f"Error creating storage directories: {str(e)}")
        return False
    
    logger.info("Setup completed successfully!")
    return True

if __name__ == "__main__":
    setup_database()
