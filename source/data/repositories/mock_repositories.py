"""
Mock repository implementations for development and testing.
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from data.repositories.base import ICustomerRepository, IUserRepository, IEmailLogRepository, IRoleRepository
from data.models.customer import Customer
from data.models.user import User, Role
from data.models.email_log import EmailLog


class MockCustomerRepository(ICustomerRepository):
    """Mock implementation of customer repository."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._customers: Dict[int, Customer] = {}
        self._next_id = 1
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample customer data."""
        sample_customers = [
            Customer(
                customer_id=1,
                first_name="John",
                last_name="Doe",
                company_name="Acme Corp",
                title="CEO",
                email="john.doe@acme.com",
                linkedin_url="https://linkedin.com/in/johndoe",
                is_active=True,
                created_date=datetime.now(),
                modified_date=datetime.now()
            ),
            Customer(
                customer_id=2,
                first_name="Jane",
                last_name="Smith",
                company_name="Tech Solutions Inc",
                title="CTO",
                email="jane.smith@techsolutions.com",
                linkedin_url="https://linkedin.com/in/janesmith",
                is_active=True,
                created_date=datetime.now(),
                modified_date=datetime.now()
            ),
            Customer(
                customer_id=3,
                first_name="Bob",
                last_name="Johnson",
                company_name="Healthcare Plus",
                title="Director of IT",
                email="bob.johnson@healthcareplus.com",
                linkedin_url="https://linkedin.com/in/bobjohnson",
                is_active=False,  # Soft deleted
                created_date=datetime.now(),
                modified_date=datetime.now()
            )
        ]
        
        for customer in sample_customers:
            self._customers[customer.customer_id] = customer
            if customer.customer_id >= self._next_id:
                self._next_id = customer.customer_id + 1
    
    def get_all(self) -> List[Customer]:
        """Get all customers."""
        return list(self._customers.values())
    
    def get_by_id(self, entity_id: int) -> Optional[Customer]:
        """Get customer by ID."""
        return self._customers.get(entity_id)
    
    def get_active_customers(self) -> List[Customer]:
        """Get all active customers."""
        return [c for c in self._customers.values() if c.is_active]
    
    def get_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email address."""
        for customer in self._customers.values():
            if customer.email.lower() == email.lower():
                return customer
        return None
    
    def create(self, entity: Customer) -> Customer:
        """Create a new customer."""
        entity.customer_id = self._next_id
        entity.created_date = datetime.now()
        entity.modified_date = datetime.now()
        self._customers[self._next_id] = entity
        self._next_id += 1
        self.logger.info(f"Created customer: {entity}")
        return entity
    
    def update(self, entity: Customer) -> Customer:
        """Update an existing customer."""
        if entity.customer_id not in self._customers:
            raise ValueError(f"Customer with ID {entity.customer_id} not found")
        
        entity.modified_date = datetime.now()
        self._customers[entity.customer_id] = entity
        self.logger.info(f"Updated customer: {entity}")
        return entity
    
    def delete(self, entity_id: int) -> bool:
        """Hard delete a customer."""
        if entity_id in self._customers:
            del self._customers[entity_id]
            self.logger.info(f"Deleted customer with ID: {entity_id}")
            return True
        return False
    
    def soft_delete(self, customer_id: int) -> bool:
        """Soft delete a customer."""
        customer = self._customers.get(customer_id)
        if customer:
            customer.is_active = False
            customer.modified_date = datetime.now()
            self.logger.info(f"Soft deleted customer: {customer}")
            return True
        return False


class MockUserRepository(IUserRepository):
    """Mock implementation of user repository."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._users: Dict[int, User] = {}
        self._next_id = 1
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample user data."""
        # Create default admin user
        admin_user = User(
            user_id=1,
            username="admin",
            email="admin@mycrm.com",
            first_name="System",
            last_name="Administrator",
            role_id=1,  # Administrator role
            is_active=True,
            created_date=datetime.now(),
            modified_date=datetime.now()
        )
        admin_user.set_password("admin123")
        
        # Create default standard user
        standard_user = User(
            user_id=2,
            username="user",
            email="user@mycrm.com",
            first_name="Standard",
            last_name="User",
            role_id=2,  # Standard user role
            is_active=True,
            created_date=datetime.now(),
            modified_date=datetime.now()
        )
        standard_user.set_password("user123")
        
        self._users[1] = admin_user
        self._users[2] = standard_user
        self._next_id = 3
    
    def get_all(self) -> List[User]:
        """Get all users."""
        return list(self._users.values())
    
    def get_by_id(self, entity_id: int) -> Optional[User]:
        """Get user by ID."""
        return self._users.get(entity_id)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        for user in self._users.values():
            if user.username.lower() == username.lower():
                return user
        return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address."""
        for user in self._users.values():
            if user.email.lower() == email.lower():
                return user
        return None
    
    def create(self, entity: User) -> User:
        """Create a new user."""
        entity.user_id = self._next_id
        entity.created_date = datetime.now()
        entity.modified_date = datetime.now()
        self._users[self._next_id] = entity
        self._next_id += 1
        self.logger.info(f"Created user: {entity}")
        return entity
    
    def update(self, entity: User) -> User:
        """Update an existing user."""
        if entity.user_id not in self._users:
            raise ValueError(f"User with ID {entity.user_id} not found")
        
        entity.modified_date = datetime.now()
        self._users[entity.user_id] = entity
        self.logger.info(f"Updated user: {entity}")
        return entity
    
    def delete(self, entity_id: int) -> bool:
        """Delete a user."""
        if entity_id in self._users:
            del self._users[entity_id]
            self.logger.info(f"Deleted user with ID: {entity_id}")
            return True
        return False
    
    def update_last_login(self, user_id: int) -> bool:
        """Update user's last login date."""
        user = self._users.get(user_id)
        if user:
            user.last_login_date = datetime.now()
            self.logger.info(f"Updated last login for user: {user.username}")
            return True
        return False


class MockEmailLogRepository(IEmailLogRepository):
    """Mock implementation of email log repository."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._email_logs: Dict[int, EmailLog] = {}
        self._next_id = 1
    
    def get_all(self) -> List[EmailLog]:
        """Get all email logs."""
        return list(self._email_logs.values())
    
    def get_by_id(self, entity_id: int) -> Optional[EmailLog]:
        """Get email log by ID."""
        return self._email_logs.get(entity_id)
    
    def get_by_customer_id(self, customer_id: int) -> List[EmailLog]:
        """Get email logs for a specific customer."""
        return [log for log in self._email_logs.values() if log.customer_id == customer_id]
    
    def get_by_user_id(self, user_id: int) -> List[EmailLog]:
        """Get email logs created by a specific user."""
        return [log for log in self._email_logs.values() if log.user_id == user_id]
    
    def get_sent_emails(self) -> List[EmailLog]:
        """Get all sent emails."""
        return [log for log in self._email_logs.values() if log.email_sent]
    
    def create(self, entity: EmailLog) -> EmailLog:
        """Create a new email log."""
        entity.email_log_id = self._next_id
        entity.created_date = datetime.now()
        self._email_logs[self._next_id] = entity
        self._next_id += 1
        self.logger.info(f"Created email log: {entity}")
        return entity
    
    def update(self, entity: EmailLog) -> EmailLog:
        """Update an existing email log."""
        if entity.email_log_id not in self._email_logs:
            raise ValueError(f"Email log with ID {entity.email_log_id} not found")
        
        self._email_logs[entity.email_log_id] = entity
        self.logger.info(f"Updated email log: {entity}")
        return entity
    
    def delete(self, entity_id: int) -> bool:
        """Delete an email log."""
        if entity_id in self._email_logs:
            del self._email_logs[entity_id]
            self.logger.info(f"Deleted email log with ID: {entity_id}")
            return True
        return False


class MockRoleRepository(IRoleRepository):
    """Mock implementation of role repository."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._roles: Dict[int, Role] = {
            1: Role(role_id=1, role_name="Administrator", description="Full system access"),
            2: Role(role_id=2, role_name="Standard User", description="Read-only access")
        }
    
    def get_all(self) -> List[Role]:
        """Get all roles."""
        return list(self._roles.values())
    
    def get_by_id(self, entity_id: int) -> Optional[Role]:
        """Get role by ID."""
        return self._roles.get(entity_id)
    
    def get_by_name(self, role_name: str) -> Optional[Role]:
        """Get role by name."""
        for role in self._roles.values():
            if role.role_name.lower() == role_name.lower():
                return role
        return None
    
    def create(self, entity: Role) -> Role:
        """Create a new role."""
        self._roles[entity.role_id] = entity
        self.logger.info(f"Created role: {entity}")
        return entity
    
    def update(self, entity: Role) -> Role:
        """Update an existing role."""
        if entity.role_id not in self._roles:
            raise ValueError(f"Role with ID {entity.role_id} not found")
        
        self._roles[entity.role_id] = entity
        self.logger.info(f"Updated role: {entity}")
        return entity
    
    def delete(self, entity_id: int) -> bool:
        """Delete a role."""
        if entity_id in self._roles and entity_id > 2:  # Don't delete default roles
            del self._roles[entity_id]
            self.logger.info(f"Deleted role with ID: {entity_id}")
            return True
        return False
