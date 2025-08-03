#!/usr/bin/env python3
"""
Script to create the CRMDb database.
"""

import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.database import DatabaseConfig
import pyodbc

def create_database():
    """Create the CRMDb database."""
    try:
        # Get database configuration
        db_config = DatabaseConfig()
        database_name = 'CRMDb'
        
        # Connect to master database to create our database
        master_config = db_config.config.copy()
        master_config['database'] = 'master'
        master_conn_string = db_config._build_connection_string_with_config(master_config)
        
        print(f"Connecting to master database...")
        with pyodbc.connect(master_conn_string, autocommit=True) as conn:
            cursor = conn.cursor()
            
            # Check if database exists
            cursor.execute("SELECT name FROM sys.databases WHERE name = ?", database_name)
            if cursor.fetchone():
                print(f"Database {database_name} already exists")
            else:
                print(f"Creating database: {database_name}")
                cursor.execute(f"CREATE DATABASE [{database_name}]")
                print(f"Database {database_name} created successfully!")
                
    except Exception as e:
        print(f"Error creating database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Creating CRMDb Database")
    print("=" * 30)
    
    success = create_database()
    if success:
        print("\nDatabase creation completed!")
        print("You can now run: python database\\database_setup.py setup")
    else:
        print("\nDatabase creation failed!")
        sys.exit(1)
