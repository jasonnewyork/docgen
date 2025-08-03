#!/usr/bin/env python3
"""
Debug script to check what's in the database.
"""

import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.database import DatabaseConfig
import pyodbc

def debug_database():
    """Debug what's in the database."""
    try:
        db_config = DatabaseConfig()
        conn_string = db_config.connection_string
        print(f"Connection string: {conn_string}")
        
        with pyodbc.connect(conn_string) as conn:
            cursor = conn.cursor()
            
            # Check what database we're connected to
            cursor.execute("SELECT DB_NAME()")
            db_name = cursor.fetchone()[0]
            print(f"Connected to database: {db_name}")
            
            # List all tables
            cursor.execute("""
                SELECT TABLE_SCHEMA, TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_SCHEMA, TABLE_NAME
            """)
            
            tables = cursor.fetchall()
            print(f"\nFound {len(tables)} tables:")
            for schema, table in tables:
                print(f"  {schema}.{table}")
            
            # Check for our specific tables
            our_tables = ['roles', 'users', 'customers', 'email_logs']
            print(f"\nChecking for our tables:")
            for table in our_tables:
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_NAME = ?
                """, table)
                count = cursor.fetchone()[0]
                print(f"  {table}: {'EXISTS' if count > 0 else 'MISSING'}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_database()
