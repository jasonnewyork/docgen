"""
Database setup utility for MyCRM application.
"""

import os
import sys
import logging

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config.database import DatabaseConfig
import pyodbc


def setup_database():
    """Set up the database schema and initial data."""
    logger = logging.getLogger(__name__)
    
    try:
        # Get database configuration
        db_config = DatabaseConfig()
        database_name = db_config.config['database']
        
        # First, try to create the database if it doesn't exist
        try:
            # Connect to master database to create our database
            master_config = db_config.config.copy()
            master_config['database'] = 'master'
            master_conn_string = db_config._build_connection_string_with_config(master_config)
            
            with pyodbc.connect(master_conn_string) as conn:
                cursor = conn.cursor()
                # Check if database exists
                cursor.execute("SELECT name FROM sys.databases WHERE name = ?", database_name)
                if not cursor.fetchone():
                    logger.info(f"Creating database: {database_name}")
                    cursor.execute(f"CREATE DATABASE [{database_name}]")
                    conn.commit()
                else:
                    logger.info(f"Database {database_name} already exists")
        except Exception as e:
            logger.warning(f"Could not create database (might already exist): {e}")
        
        # Read schema script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        schema_file = os.path.join(script_dir, 'schema.sql')
        
        if not os.path.exists(schema_file):
            logger.error(f"Schema file not found: {schema_file}")
            return False
        
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Connect to our target database
        conn_string = db_config.connection_string
        logger.info(f"Connecting to database: {database_name}...")
        
        with pyodbc.connect(conn_string) as conn:
            cursor = conn.cursor()
            
            # Split script into individual statements
            statements = [stmt.strip() for stmt in schema_sql.split('GO') if stmt.strip()]
            
            logger.info(f"Found {len(statements)} SQL statements to execute")
            
            for i, statement in enumerate(statements, 1):
                if statement and statement.strip():
                    # Remove leading/trailing whitespace and comments
                    clean_statement = statement.strip()
                    
                    # Skip empty statements or those that are only comments
                    lines = [line.strip() for line in clean_statement.split('\n') if line.strip()]
                    non_comment_lines = [line for line in lines if not line.startswith('--')]
                    
                    if not non_comment_lines:
                        logger.info(f"Skipping statement {i}: only comments")
                        continue
                    
                    # Reconstruct statement without comment-only lines
                    clean_statement = '\n'.join(lines)
                    
                    try:
                        # Skip PRINT statements as they're not supported the same way
                        if clean_statement.upper().startswith('PRINT'):
                            print(clean_statement.replace('PRINT ', '').strip("';"))
                            continue
                        
                        logger.info(f"Executing statement {i}: {clean_statement[:50]}...")
                        cursor.execute(clean_statement)
                        cursor.commit()  # Commit each statement immediately
                        logger.info(f"Statement {i} executed and committed successfully")
                        
                    except pyodbc.Error as e:
                        # Some errors might be expected (like table already exists)
                        if "already exists" in str(e).lower():
                            logger.warning(f"Object already exists in statement {i}: {e}")
                        else:
                            logger.error(f"Error executing statement {i}: {e}")
                            logger.error(f"Statement: {clean_statement}")
                            raise  # Re-raise the error to stop execution
        
        logger.info("Database setup completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        return False


def check_database_connection():
    """Check if database connection is working."""
    logger = logging.getLogger(__name__)
    
    try:
        db_config = DatabaseConfig()
        conn_string = db_config.connection_string
        
        with pyodbc.connect(conn_string) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
            if result:
                logger.info("Database connection successful!")
                return True
            else:
                logger.error("Database connection failed - no result")
                return False
                
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


def verify_schema():
    """Verify that all required tables exist."""
    logger = logging.getLogger(__name__)
    
    required_tables = ['roles', 'users', 'customers', 'email_logs']
    
    try:
        db_config = DatabaseConfig()
        conn_string = db_config.connection_string
        
        with pyodbc.connect(conn_string) as conn:
            cursor = conn.cursor()
            
            # Check each required table
            missing_tables = []
            for table in required_tables:
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_NAME = ?
                """, table)
                
                count = cursor.fetchone()[0]
                if count == 0:
                    missing_tables.append(table)
            
            if missing_tables:
                logger.error(f"Missing tables: {', '.join(missing_tables)}")
                return False
            else:
                logger.info("All required tables exist!")
                return True
                
    except Exception as e:
        logger.error(f"Schema verification failed: {e}")
        return False


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("MyCRM Database Setup Utility")
    print("=" * 40)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'setup':
            print("Setting up database schema...")
            success = setup_database()
            if success:
                print("Database setup completed successfully!")
            else:
                print("Database setup failed. Check logs for details.")
                sys.exit(1)
                
        elif command == 'check':
            print("Checking database connection...")
            success = check_database_connection()
            if success:
                print("Database connection successful!")
            else:
                print("Database connection failed. Check configuration.")
                sys.exit(1)
                
        elif command == 'verify':
            print("Verifying database schema...")
            success = verify_schema()
            if success:
                print("Database schema verification successful!")
            else:
                print("Database schema verification failed.")
                sys.exit(1)
        else:
            print(f"Unknown command: {command}")
            print("Usage: python database_setup.py [setup|check|verify]")
            sys.exit(1)
    else:
        print("Usage: python database_setup.py [setup|check|verify]")
        print("")
        print("Commands:")
        print("  setup  - Create database schema and insert initial data")
        print("  check  - Test database connection")
        print("  verify - Verify that all required tables exist")
        sys.exit(1)
