"""
Repository factory for creating appropriate repository instances.
Implements automatic fallback from SQL Server to mock repositories.
"""

import logging
from typing import Dict, Any
from config.database import db_config
from data.repositories.base import ICustomerRepository, IUserRepository, IEmailLogRepository, IRoleRepository
from data.repositories.mock_repositories import (
    MockCustomerRepository, 
    MockUserRepository, 
    MockEmailLogRepository, 
    MockRoleRepository
)


class RepositoryFactory:
    """Factory for creating repository instances with automatic fallback."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._use_sql = None
        self._repositories: Dict[str, Any] = {}
        self._test_database_availability()
    
    def _test_database_availability(self):
        """Test if SQL Server database is available."""
        try:
            self._use_sql = db_config.test_connection()
            if self._use_sql:
                self.logger.info("SQL Server database available - using SQL repositories")
            else:
                self.logger.warning("SQL Server database unavailable - using mock repositories")
        except Exception as e:
            self.logger.error(f"Error testing database connection: {e}")
            self._use_sql = False
    
    @property
    def is_using_sql(self) -> bool:
        """Check if factory is using SQL repositories."""
        return self._use_sql == True
    
    def get_customer_repository(self) -> ICustomerRepository:
        """Get customer repository instance."""
        if 'customer' not in self._repositories:
            if self._use_sql:
                try:
                    # Import here to avoid circular dependencies
                    from data.repositories.sql_repositories import SqlCustomerRepository
                    self._repositories['customer'] = SqlCustomerRepository()
                    self.logger.info("Created SQL customer repository")
                except Exception as e:
                    self.logger.error(f"Failed to create SQL customer repository: {e}")
                    self.logger.info("Falling back to mock customer repository")
                    self._repositories['customer'] = MockCustomerRepository()
            else:
                self._repositories['customer'] = MockCustomerRepository()
                self.logger.info("Created mock customer repository")
        
        return self._repositories['customer']
    
    def get_user_repository(self) -> IUserRepository:
        """Get user repository instance."""
        if 'user' not in self._repositories:
            if self._use_sql:
                try:
                    from data.repositories.sql_repositories import SqlUserRepository
                    self._repositories['user'] = SqlUserRepository()
                    self.logger.info("Created SQL user repository")
                except Exception as e:
                    self.logger.error(f"Failed to create SQL user repository: {e}")
                    self.logger.info("Falling back to mock user repository")
                    self._repositories['user'] = MockUserRepository()
            else:
                self._repositories['user'] = MockUserRepository()
                self.logger.info("Created mock user repository")
        
        return self._repositories['user']
    
    def get_email_log_repository(self) -> IEmailLogRepository:
        """Get email log repository instance."""
        if 'email_log' not in self._repositories:
            if self._use_sql:
                try:
                    from data.repositories.sql_repositories import SqlEmailLogRepository
                    self._repositories['email_log'] = SqlEmailLogRepository()
                    self.logger.info("Created SQL email log repository")
                except Exception as e:
                    self.logger.error(f"Failed to create SQL email log repository: {e}")
                    self.logger.info("Falling back to mock email log repository")
                    self._repositories['email_log'] = MockEmailLogRepository()
            else:
                self._repositories['email_log'] = MockEmailLogRepository()
                self.logger.info("Created mock email log repository")
        
        return self._repositories['email_log']
    
    def get_role_repository(self) -> IRoleRepository:
        """Get role repository instance."""
        if 'role' not in self._repositories:
            if self._use_sql:
                try:
                    from data.repositories.sql_repositories import SqlRoleRepository
                    self._repositories['role'] = SqlRoleRepository()
                    self.logger.info("Created SQL role repository")
                except Exception as e:
                    self.logger.error(f"Failed to create SQL role repository: {e}")
                    self.logger.info("Falling back to mock role repository")
                    self._repositories['role'] = MockRoleRepository()
            else:
                self._repositories['role'] = MockRoleRepository()
                self.logger.info("Created mock role repository")
        
        return self._repositories['role']
    
    def reset(self):
        """Reset factory - clears cached repositories and retests database."""
        self._repositories.clear()
        self._test_database_availability()
        self.logger.info("Repository factory reset")


# Global repository factory instance
repository_factory = RepositoryFactory()
