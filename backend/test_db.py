"""
Test script for database setup.
"""
from backend.database.db import init_db, get_db_connection
from backend.utils.file_storage import ensure_storage_dirs

def test_db_setup():
    # Initialize the database
    print("Initializing database...")
    init_db()

    # Check if tables were created
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:")
    for table in tables:
        print(f"- {table['name']}")

    # Initialize storage directories
    print("\nInitializing storage directories...")
    ensure_storage_dirs()

    print("\nSetup complete!")

if __name__ == "__main__":
    test_db_setup()
