"""
SQL repository implementations for SQL Server.
"""

import pyodbc
import logging
from typing import List, Optional
from datetime import datetime
from data.models.customer import Customer
from data.models.user import User, Role
from data.models.email_log import EmailLog
from data.repositories.base import BaseRepository
from config.database import DatabaseConfig


class SqlCustomerRepository(BaseRepository):
    """SQL Server implementation of customer repository."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_config = DatabaseConfig()
    
    def _get_connection(self):
        """Get database connection."""
        return pyodbc.connect(self.db_config.get_connection_string())
    
    def get_all(self) -> List[Customer]:
        """Get all customers."""
        customers = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT customer_id, company_name, contact_first_name, contact_last_name,
                           contact_email, contact_phone, address, city, state, country,
                           postal_code, industry, created_date, last_modified_date, is_active
                    FROM customers
                    ORDER BY company_name
                """)
                
                for row in cursor.fetchall():
                    customer = Customer(
                        customer_id=row.customer_id,
                        company_name=row.company_name,
                        contact_first_name=row.contact_first_name,
                        contact_last_name=row.contact_last_name,
                        contact_email=row.contact_email,
                        contact_phone=row.contact_phone,
                        address=row.address,
                        city=row.city,
                        state=row.state,
                        country=row.country,
                        postal_code=row.postal_code,
                        industry=row.industry,
                        created_date=row.created_date,
                        last_modified_date=row.last_modified_date,
                        is_active=row.is_active
                    )
                    customers.append(customer)
                    
        except Exception as e:
            self.logger.error(f"Error getting all customers: {e}")
            raise
            
        return customers
    
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """Get customer by ID."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT customer_id, company_name, contact_first_name, contact_last_name,
                           contact_email, contact_phone, address, city, state, country,
                           postal_code, industry, created_date, last_modified_date, is_active
                    FROM customers
                    WHERE customer_id = ?
                """, customer_id)
                
                row = cursor.fetchone()
                if row:
                    return Customer(
                        customer_id=row.customer_id,
                        company_name=row.company_name,
                        contact_first_name=row.contact_first_name,
                        contact_last_name=row.contact_last_name,
                        contact_email=row.contact_email,
                        contact_phone=row.contact_phone,
                        address=row.address,
                        city=row.city,
                        state=row.state,
                        country=row.country,
                        postal_code=row.postal_code,
                        industry=row.industry,
                        created_date=row.created_date,
                        last_modified_date=row.last_modified_date,
                        is_active=row.is_active
                    )
                    
        except Exception as e:
            self.logger.error(f"Error getting customer by ID {customer_id}: {e}")
            raise
            
        return None
    
    def create(self, customer: Customer) -> Customer:
        """Create new customer."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO customers (
                        company_name, contact_first_name, contact_last_name,
                        contact_email, contact_phone, address, city, state, country,
                        postal_code, industry, created_date, last_modified_date, is_active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    customer.company_name,
                    customer.contact_first_name,
                    customer.contact_last_name,
                    customer.contact_email,
                    customer.contact_phone,
                    customer.address,
                    customer.city,
                    customer.state,
                    customer.country,
                    customer.postal_code,
                    customer.industry,
                    datetime.now(),
                    datetime.now(),
                    True
                ))
                
                # Get the inserted ID
                cursor.execute("SELECT @@IDENTITY")
                customer_id = cursor.fetchone()[0]
                conn.commit()
                
                # Return the created customer
                return self.get_by_id(customer_id)
                
        except Exception as e:
            self.logger.error(f"Error creating customer: {e}")
            raise
    
    def update(self, customer: Customer) -> bool:
        """Update existing customer."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE customers SET
                        company_name = ?, contact_first_name = ?, contact_last_name = ?,
                        contact_email = ?, contact_phone = ?, address = ?, city = ?, 
                        state = ?, country = ?, postal_code = ?, industry = ?,
                        last_modified_date = ?, is_active = ?
                    WHERE customer_id = ?
                """, (
                    customer.company_name,
                    customer.contact_first_name,
                    customer.contact_last_name,
                    customer.contact_email,
                    customer.contact_phone,
                    customer.address,
                    customer.city,
                    customer.state,
                    customer.country,
                    customer.postal_code,
                    customer.industry,
                    datetime.now(),
                    customer.is_active,
                    customer.customer_id
                ))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            self.logger.error(f"Error updating customer: {e}")
            raise
    
    def delete(self, customer_id: int) -> bool:
        """Delete customer (soft delete)."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE customers SET is_active = 0, last_modified_date = ?
                    WHERE customer_id = ?
                """, (datetime.now(), customer_id))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            self.logger.error(f"Error deleting customer: {e}")
            raise
    
    def search(self, query: str) -> List[Customer]:
        """Search customers by name, email, or company."""
        customers = []
        try:
            search_term = f"%{query}%"
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT customer_id, company_name, contact_first_name, contact_last_name,
                           contact_email, contact_phone, address, city, state, country,
                           postal_code, industry, created_date, last_modified_date, is_active
                    FROM customers
                    WHERE (company_name LIKE ? OR contact_first_name LIKE ? OR 
                           contact_last_name LIKE ? OR contact_email LIKE ?)
                           AND is_active = 1
                    ORDER BY company_name
                """, (search_term, search_term, search_term, search_term))
                
                for row in cursor.fetchall():
                    customer = Customer(
                        customer_id=row.customer_id,
                        company_name=row.company_name,
                        contact_first_name=row.contact_first_name,
                        contact_last_name=row.contact_last_name,
                        contact_email=row.contact_email,
                        contact_phone=row.contact_phone,
                        address=row.address,
                        city=row.city,
                        state=row.state,
                        country=row.country,
                        postal_code=row.postal_code,
                        industry=row.industry,
                        created_date=row.created_date,
                        last_modified_date=row.last_modified_date,
                        is_active=row.is_active
                    )
                    customers.append(customer)
                    
        except Exception as e:
            self.logger.error(f"Error searching customers: {e}")
            raise
            
        return customers


class SqlUserRepository(BaseRepository):
    """SQL Server implementation of user repository."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_config = DatabaseConfig()
    
    def _get_connection(self):
        """Get database connection."""
        return pyodbc.connect(self.db_config.get_connection_string())
    
    def get_all(self) -> List[User]:
        """Get all users."""
        users = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT user_id, username, email, first_name, last_name,
                           password_hash, role_id, is_active, created_date, last_login_date
                    FROM users
                    ORDER BY username
                """)
                
                for row in cursor.fetchall():
                    user = User(
                        user_id=row.user_id,
                        username=row.username,
                        email=row.email,
                        first_name=row.first_name,
                        last_name=row.last_name,
                        password_hash=row.password_hash,
                        role_id=row.role_id,
                        is_active=row.is_active,
                        created_date=row.created_date,
                        last_login_date=row.last_login_date
                    )
                    users.append(user)
                    
        except Exception as e:
            self.logger.error(f"Error getting all users: {e}")
            raise
            
        return users
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT user_id, username, email, first_name, last_name,
                           password_hash, role_id, is_active, created_date, last_login_date
                    FROM users
                    WHERE user_id = ?
                """, user_id)
                
                row = cursor.fetchone()
                if row:
                    return User(
                        user_id=row.user_id,
                        username=row.username,
                        email=row.email,
                        first_name=row.first_name,
                        last_name=row.last_name,
                        password_hash=row.password_hash,
                        role_id=row.role_id,
                        is_active=row.is_active,
                        created_date=row.created_date,
                        last_login_date=row.last_login_date
                    )
                    
        except Exception as e:
            self.logger.error(f"Error getting user by ID {user_id}: {e}")
            raise
            
        return None
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT user_id, username, email, first_name, last_name,
                           password_hash, role_id, is_active, created_date, last_login_date
                    FROM users
                    WHERE username = ?
                """, username)
                
                row = cursor.fetchone()
                if row:
                    return User(
                        user_id=row.user_id,
                        username=row.username,
                        email=row.email,
                        first_name=row.first_name,
                        last_name=row.last_name,
                        password_hash=row.password_hash,
                        role_id=row.role_id,
                        is_active=row.is_active,
                        created_date=row.created_date,
                        last_login_date=row.last_login_date
                    )
                    
        except Exception as e:
            self.logger.error(f"Error getting user by username {username}: {e}")
            raise
            
        return None
    
    def create(self, user: User) -> User:
        """Create new user."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (
                        username, email, first_name, last_name,
                        password_hash, role_id, is_active, created_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user.username,
                    user.email,
                    user.first_name,
                    user.last_name,
                    user.password_hash,
                    user.role_id,
                    True,
                    datetime.now()
                ))
                
                # Get the inserted ID
                cursor.execute("SELECT @@IDENTITY")
                user_id = cursor.fetchone()[0]
                conn.commit()
                
                # Return the created user
                return self.get_by_id(user_id)
                
        except Exception as e:
            self.logger.error(f"Error creating user: {e}")
            raise
    
    def update(self, user: User) -> bool:
        """Update existing user."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET
                        username = ?, email = ?, first_name = ?, last_name = ?,
                        role_id = ?, is_active = ?
                    WHERE user_id = ?
                """, (
                    user.username,
                    user.email,
                    user.first_name,
                    user.last_name,
                    user.role_id,
                    user.is_active,
                    user.user_id
                ))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            self.logger.error(f"Error updating user: {e}")
            raise
    
    def update_password(self, user_id: int, password_hash: str) -> bool:
        """Update user password."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET password_hash = ?
                    WHERE user_id = ?
                """, (password_hash, user_id))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            self.logger.error(f"Error updating password for user {user_id}: {e}")
            raise
    
    def update_last_login(self, user_id: int) -> bool:
        """Update user's last login date."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET last_login_date = ?
                    WHERE user_id = ?
                """, (datetime.now(), user_id))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            self.logger.error(f"Error updating last login for user {user_id}: {e}")
            raise
    
    def delete(self, user_id: int) -> bool:
        """Delete user (soft delete)."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET is_active = 0
                    WHERE user_id = ?
                """, user_id)
                
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            self.logger.error(f"Error deleting user: {e}")
            raise


class SqlRoleRepository(BaseRepository):
    """SQL Server implementation of role repository."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_config = DatabaseConfig()
    
    def _get_connection(self):
        """Get database connection."""
        return pyodbc.connect(self.db_config.get_connection_string())
    
    def get_all(self) -> List[Role]:
        """Get all roles."""
        roles = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT role_id, role_name, description
                    FROM roles
                    ORDER BY role_id
                """)
                
                for row in cursor.fetchall():
                    role = Role(
                        role_id=row.role_id,
                        role_name=row.role_name,
                        description=row.description
                    )
                    roles.append(role)
                    
        except Exception as e:
            self.logger.error(f"Error getting all roles: {e}")
            raise
            
        return roles
    
    def get_by_id(self, role_id: int) -> Optional[Role]:
        """Get role by ID."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT role_id, role_name, description
                    FROM roles
                    WHERE role_id = ?
                """, role_id)
                
                row = cursor.fetchone()
                if row:
                    return Role(
                        role_id=row.role_id,
                        role_name=row.role_name,
                        description=row.description
                    )
                    
        except Exception as e:
            self.logger.error(f"Error getting role by ID {role_id}: {e}")
            raise
            
        return None


class SqlEmailLogRepository(BaseRepository):
    """SQL Server implementation of email log repository."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_config = DatabaseConfig()
    
    def _get_connection(self):
        """Get database connection."""
        return pyodbc.connect(self.db_config.get_connection_string())
    
    def get_all(self) -> List[EmailLog]:
        """Get all email logs."""
        logs = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT log_id, customer_id, user_id, email_type, subject,
                           content, recipient_email, sent_date, status, error_message
                    FROM email_logs
                    ORDER BY sent_date DESC
                """)
                
                for row in cursor.fetchall():
                    log = EmailLog(
                        log_id=row.log_id,
                        customer_id=row.customer_id,
                        user_id=row.user_id,
                        email_type=row.email_type,
                        subject=row.subject,
                        content=row.content,
                        recipient_email=row.recipient_email,
                        sent_date=row.sent_date,
                        status=row.status,
                        error_message=row.error_message
                    )
                    logs.append(log)
                    
        except Exception as e:
            self.logger.error(f"Error getting all email logs: {e}")
            raise
            
        return logs
    
    def get_by_id(self, log_id: int) -> Optional[EmailLog]:
        """Get email log by ID."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT log_id, customer_id, user_id, email_type, subject,
                           content, recipient_email, sent_date, status, error_message
                    FROM email_logs
                    WHERE log_id = ?
                """, log_id)
                
                row = cursor.fetchone()
                if row:
                    return EmailLog(
                        log_id=row.log_id,
                        customer_id=row.customer_id,
                        user_id=row.user_id,
                        email_type=row.email_type,
                        subject=row.subject,
                        content=row.content,
                        recipient_email=row.recipient_email,
                        sent_date=row.sent_date,
                        status=row.status,
                        error_message=row.error_message
                    )
                    
        except Exception as e:
            self.logger.error(f"Error getting email log by ID {log_id}: {e}")
            raise
            
        return None
    
    def get_by_customer(self, customer_id: int) -> List[EmailLog]:
        """Get email logs by customer."""
        logs = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT log_id, customer_id, user_id, email_type, subject,
                           content, recipient_email, sent_date, status, error_message
                    FROM email_logs
                    WHERE customer_id = ?
                    ORDER BY sent_date DESC
                """, customer_id)
                
                for row in cursor.fetchall():
                    log = EmailLog(
                        log_id=row.log_id,
                        customer_id=row.customer_id,
                        user_id=row.user_id,
                        email_type=row.email_type,
                        subject=row.subject,
                        content=row.content,
                        recipient_email=row.recipient_email,
                        sent_date=row.sent_date,
                        status=row.status,
                        error_message=row.error_message
                    )
                    logs.append(log)
                    
        except Exception as e:
            self.logger.error(f"Error getting email logs by customer {customer_id}: {e}")
            raise
            
        return logs
    
    def create(self, log: EmailLog) -> EmailLog:
        """Create new email log."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO email_logs (
                        customer_id, user_id, email_type, subject, content,
                        recipient_email, sent_date, status, error_message
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    log.customer_id,
                    log.user_id,
                    log.email_type,
                    log.subject,
                    log.content,
                    log.recipient_email,
                    datetime.now(),
                    log.status,
                    log.error_message
                ))
                
                # Get the inserted ID
                cursor.execute("SELECT @@IDENTITY")
                log_id = cursor.fetchone()[0]
                conn.commit()
                
                # Return the created log
                return self.get_by_id(log_id)
                
        except Exception as e:
            self.logger.error(f"Error creating email log: {e}")
            raise
    
    def update_status(self, log_id: int, status: str, error_message: str = None) -> bool:
        """Update email log status."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE email_logs SET status = ?, error_message = ?
                    WHERE log_id = ?
                """, (status, error_message, log_id))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            self.logger.error(f"Error updating email log status: {e}")
            raise
