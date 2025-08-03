"""
Database configuration and connection management.
"""

import logging
import pyodbc
from typing import Optional, Dict, Any
from config.settings import get_database_config


class DatabaseConfig:
    """Database configuration and connection manager."""
    
    def __init__(self):
        self.config = get_database_config()
        self.logger = logging.getLogger(__name__)
        self._connection_string: Optional[str] = None
    
    @property
    def connection_string(self) -> str:
        """Get the database connection string."""
        if self._connection_string is None:
            self._connection_string = self._build_connection_string()
        return self._connection_string
    
    def _build_connection_string(self) -> str:
        """Build the SQL Server connection string."""
        return self._build_connection_string_with_config(self.config)
    
    def _build_connection_string_with_config(self, config: Dict[str, Any]) -> str:
        """Build the SQL Server connection string with provided config."""
        parts = [
            f"DRIVER={{{config['driver']}}}",
            f"SERVER={config['server']}",
            f"DATABASE={config['database']}"
        ]
        
        if config['trusted_connection'].lower() == 'yes':
            parts.append("Trusted_Connection=yes")
        else:
            parts.append(f"UID={config['username']}")
            if config['password']:
                parts.append(f"PWD={config['password']}")
        
        parts.append(f"Connection Timeout={config['connection_timeout']}")
        
        return ';'.join(parts)
    
    def test_connection(self) -> bool:
        """Test if database connection is available."""
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                self.logger.info("Database connection test successful")
                return True
        except Exception as e:
            self.logger.warning(f"Database connection test failed: {e}")
            return False
    
    def get_connection(self) -> pyodbc.Connection:
        """Get a database connection."""
        try:
            conn = pyodbc.connect(self.connection_string)
            conn.timeout = self.config['command_timeout']
            return conn
        except Exception as e:
            self.logger.error(f"Failed to create database connection: {e}")
            raise
    
    def execute_script_file(self, script_path: str) -> bool:
        """Execute a SQL script file."""
        try:
            with open(script_path, 'r') as file:
                script = file.read()
            
            # Split script by GO statements (SQL Server batch separator)
            batches = [batch.strip() for batch in script.split('GO') if batch.strip()]
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                for batch in batches:
                    if batch:
                        cursor.execute(batch)
                conn.commit()
            
            self.logger.info(f"Successfully executed script: {script_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to execute script {script_path}: {e}")
            return False


# Global database configuration instance
db_config = DatabaseConfig()
