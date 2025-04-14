"""
Database connection and utility functions.
"""
import os
import sqlite3
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database file path
DB_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = DB_DIR / "vidgen.db"
SCHEMA_FILE = DB_DIR / "schema.sql"

def get_db_connection():
    """
    Get a connection to the SQLite database.
    
    Returns:
        sqlite3.Connection: A connection to the database
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def init_db():
    """
    Initialize the database with the schema.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create the database directory if it doesn't exist
        os.makedirs(DB_DIR, exist_ok=True)
        
        # Read the schema file
        with open(SCHEMA_FILE, 'r') as f:
            schema = f.read()
        
        # Connect to the database and execute the schema
        conn = get_db_connection()
        conn.executescript(schema)
        conn.commit()
        conn.close()
        
        logger.info(f"Database initialized at {DB_FILE}")
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        return False

def query(sql: str, params: Tuple = (), one: bool = False) -> Union[Dict, List[Dict], None]:
    """
    Execute a query and return the results.
    
    Args:
        sql: SQL query to execute
        params: Parameters for the query
        one: If True, return only one result
        
    Returns:
        The query results as a dictionary or list of dictionaries
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql, params)
        
        if one:
            result = dict(cur.fetchone()) if cur.fetchone() else None
        else:
            result = [dict(row) for row in cur.fetchall()]
            
        cur.close()
        conn.close()
        return result
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        logger.error(f"SQL: {sql}")
        logger.error(f"Params: {params}")
        return None

def execute(sql: str, params: Tuple = ()) -> Optional[int]:
    """
    Execute a SQL statement and return the last row id.
    
    Args:
        sql: SQL statement to execute
        params: Parameters for the statement
        
    Returns:
        The last row id or None if an error occurred
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        last_id = cur.lastrowid
        cur.close()
        conn.close()
        return last_id
    except Exception as e:
        logger.error(f"Error executing statement: {str(e)}")
        logger.error(f"SQL: {sql}")
        logger.error(f"Params: {params}")
        return None

def execute_many(sql: str, params_list: List[Tuple]) -> bool:
    """
    Execute a SQL statement with multiple parameter sets.
    
    Args:
        sql: SQL statement to execute
        params_list: List of parameter tuples
        
    Returns:
        True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.executemany(sql, params_list)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error executing statement: {str(e)}")
        logger.error(f"SQL: {sql}")
        return False

# Initialize the database if this module is run directly
if __name__ == "__main__":
    init_db()
