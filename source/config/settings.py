"""
Application settings and configuration management.
"""

import os
from typing import Dict, Any


def get_environment() -> str:
    """Get the current environment (development, testing, production)."""
    return os.getenv('ENVIRONMENT', 'development')


def get_database_config() -> Dict[str, Any]:
    """Get database configuration settings."""
    sql_password = os.getenv('SQL_PASSWORD')
    if not sql_password:
        raise ValueError("SQL_PASSWORD environment variable is required for database connection")
    
    return {
        'server': os.getenv('DB_SERVER', 'localhost'),
        'database': os.getenv('DB_NAME', 'CRMDb'),
        'username': os.getenv('DB_USERNAME', 'sa'),
        'password': sql_password,
        'driver': os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server'),
        'trusted_connection': os.getenv('DB_TRUSTED_CONNECTION', 'no'),
        'connection_timeout': int(os.getenv('DB_CONNECTION_TIMEOUT', '30')),
        'command_timeout': int(os.getenv('DB_COMMAND_TIMEOUT', '30'))
    }


def get_openai_config() -> Dict[str, Any]:
    """Get OpenAI configuration settings."""
    return {
        'api_key': os.getenv('OPENAI_API_KEY', ''),
        'model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
        'max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '500')),
        'temperature': float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    }


def get_email_config() -> Dict[str, Any]:
    """Get email configuration settings."""
    return {
        'smtp_server': os.getenv('SMTP_SERVER', 'localhost'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
        'smtp_username': os.getenv('SMTP_USERNAME', ''),
        'smtp_password': os.getenv('SMTP_PASSWORD', ''),
        'use_tls': os.getenv('SMTP_USE_TLS', 'true').lower() == 'true',
        'sender_email': os.getenv('SENDER_EMAIL', 'noreply@mycrm.com'),
        'sender_name': os.getenv('SENDER_NAME', 'MyCRM System')
    }


def get_security_config() -> Dict[str, Any]:
    """Get security configuration settings."""
    return {
        'session_timeout': int(os.getenv('SESSION_TIMEOUT', '3600')),  # 1 hour
        'bcrypt_rounds': int(os.getenv('BCRYPT_ROUNDS', '12')),
        'secret_key': os.getenv('SECRET_KEY', 'your-secret-key-change-in-production'),
        'enable_hipaa_compliance': os.getenv('ENABLE_HIPAA_COMPLIANCE', 'true').lower() == 'true',
        'enable_ai_compliance': os.getenv('ENABLE_AI_COMPLIANCE', 'true').lower() == 'true'
    }


def get_cherrypy_config() -> Dict[str, Any]:
    """Get CherryPy server configuration."""
    environment = get_environment()
    
    config = {
        'server.socket_host': os.getenv('HOST', '127.0.0.1'),
        'server.socket_port': int(os.getenv('PORT', '8080')),
        'server.thread_pool': int(os.getenv('THREAD_POOL', '10')),
        'engine.autoreload.on': environment == 'development',
        'log.screen': True,
        'log.error_file': 'logs/cherrypy_error.log',
        'log.access_file': 'logs/cherrypy_access.log',
        'tools.sessions.on': True,
        'tools.sessions.timeout': get_security_config()['session_timeout'] // 60,  # Convert to minutes
        'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
        'tools.sessions.storage_path': os.path.join(os.getcwd(), 'sessions'),
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(os.getcwd(), 'web', 'static'),
        'tools.staticdir.root': '/'
    }
    
    # Create required directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('sessions', exist_ok=True)
    
    return config


def get_app_config() -> Dict[str, Any]:
    """Get complete application configuration."""
    return {
        'environment': get_environment(),
        'database': get_database_config(),
        'openai': get_openai_config(),
        'email': get_email_config(),
        'security': get_security_config(),
        'cherrypy': get_cherrypy_config()
    }


# Import cherrypy here to avoid circular imports
import cherrypy
