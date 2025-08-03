"""
Base repository interface and abstract classes.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic, TYPE_CHECKING

if TYPE_CHECKING:
    from data.models.customer import Customer
    from data.models.user import User
    from data.models.email_log import EmailLog
    from data.models.user import Role

T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    """Base repository interface."""
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities."""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get entity by ID."""
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an existing entity."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete an entity by ID."""
        pass


class ICustomerRepository(IRepository):
    """Customer repository interface."""
    
    @abstractmethod
    def get_active_customers(self) -> List['Customer']:
        """Get all active customers."""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional['Customer']:
        """Get customer by email address."""
        pass
    
    @abstractmethod
    def soft_delete(self, customer_id: int) -> bool:
        """Soft delete a customer (set is_active = False)."""
        pass


class IUserRepository(IRepository):
    """User repository interface."""
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional['User']:
        """Get user by username."""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional['User']:
        """Get user by email address."""
        pass
    
    @abstractmethod
    def update_last_login(self, user_id: int) -> bool:
        """Update user's last login date."""
        pass


class IEmailLogRepository(IRepository):
    """Email log repository interface."""
    
    @abstractmethod
    def get_by_customer_id(self, customer_id: int) -> List['EmailLog']:
        """Get email logs for a specific customer."""
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List['EmailLog']:
        """Get email logs created by a specific user."""
        pass
    
    @abstractmethod
    def get_sent_emails(self) -> List['EmailLog']:
        """Get all sent emails."""
        pass


class IRoleRepository(IRepository):
    """Role repository interface."""
    
    @abstractmethod
    def get_by_name(self, role_name: str) -> Optional['Role']:
        """Get role by name."""
        pass
