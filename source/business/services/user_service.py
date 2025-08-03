"""
User service for authentication and user management.
"""

import logging
from datetime import datetime
from typing import List, Optional
from data.factory import repository_factory
from data.models.user import User, Role


class UserService:
    """Service class for user management and authentication."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.user_repository = repository_factory.get_user_repository()
        self.role_repository = repository_factory.get_role_repository()
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password."""
        try:
            user = self.user_repository.get_by_username(username)
            if user and user.is_active and user.check_password(password):
                # Update last login date
                self.user_repository.update_last_login(user.user_id)
                self.logger.info(f"User authenticated successfully: {username}")
                return user
            else:
                self.logger.warning(f"Authentication failed for username: {username}")
                return None
        except Exception as e:
            self.logger.error(f"Error authenticating user {username}: {e}")
            raise
    
    def get_all_users(self) -> List[User]:
        """Get all users."""
        try:
            users = self.user_repository.get_all()
            self.logger.info(f"Retrieved {len(users)} users")
            return users
        except Exception as e:
            self.logger.error(f"Error getting all users: {e}")
            raise
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        try:
            user = self.user_repository.get_by_id(user_id)
            if user:
                self.logger.info(f"Retrieved user: {user}")
            else:
                self.logger.warning(f"User not found with ID: {user_id}")
            return user
        except Exception as e:
            self.logger.error(f"Error getting user by ID {user_id}: {e}")
            raise
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        try:
            user = self.user_repository.get_by_username(username)
            if user:
                self.logger.info(f"Retrieved user by username: {user}")
            else:
                self.logger.warning(f"User not found with username: {username}")
            return user
        except Exception as e:
            self.logger.error(f"Error getting user by username {username}: {e}")
            raise
    
    def create_user(self, user: User, password: str) -> User:
        """Create a new user."""
        try:
            # Validate user data
            errors = user.validate()
            if errors:
                raise ValueError(f"User validation failed: {', '.join(errors)}")
            
            # Validate password
            if not password or len(password) < 6:
                raise ValueError("Password must be at least 6 characters long")
            
            # Check for duplicate username
            existing_user = self.user_repository.get_by_username(user.username)
            if existing_user:
                raise ValueError(f"User with username {user.username} already exists")
            
            # Check for duplicate email
            existing_email = self.user_repository.get_by_email(user.email)
            if existing_email:
                raise ValueError(f"User with email {user.email} already exists")
            
            # Set password
            user.set_password(password)
            
            # Create user
            created_user = self.user_repository.create(user)
            self.logger.info(f"Created user: {created_user}")
            return created_user
            
        except Exception as e:
            self.logger.error(f"Error creating user: {e}")
            raise
    
    def update_user(self, user: User) -> User:
        """Update an existing user."""
        try:
            # Validate user data
            errors = user.validate()
            if errors:
                raise ValueError(f"User validation failed: {', '.join(errors)}")
            
            # Check if user exists
            existing_user = self.user_repository.get_by_id(user.user_id)
            if not existing_user:
                raise ValueError(f"User with ID {user.user_id} not found")
            
            # Check for duplicate username (excluding current user)
            username_user = self.user_repository.get_by_username(user.username)
            if username_user and username_user.user_id != user.user_id:
                raise ValueError(f"Another user with username {user.username} already exists")
            
            # Check for duplicate email (excluding current user)
            email_user = self.user_repository.get_by_email(user.email)
            if email_user and email_user.user_id != user.user_id:
                raise ValueError(f"Another user with email {user.email} already exists")
            
            # Update user
            updated_user = self.user_repository.update(user)
            self.logger.info(f"Updated user: {updated_user}")
            return updated_user
            
        except Exception as e:
            self.logger.error(f"Error updating user: {e}")
            raise
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """Change a user's password."""
        try:
            # Get user
            user = self.user_repository.get_by_id(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            
            # Validate current password
            if not user.check_password(current_password):
                raise ValueError("Current password is incorrect")
            
            # Validate new password
            if not new_password or len(new_password) < 6:
                raise ValueError("New password must be at least 6 characters long")
            
            # Set new password and update
            user.set_password(new_password)
            self.user_repository.update(user)
            
            self.logger.info(f"Password changed for user: {user.username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error changing password for user ID {user_id}: {e}")
            raise
    
    def reset_password(self, user_id: int, new_password: str) -> bool:
        """Reset a user's password (admin function)."""
        try:
            # Get user
            user = self.user_repository.get_by_id(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            
            # Validate new password
            if not new_password or len(new_password) < 6:
                raise ValueError("New password must be at least 6 characters long")
            
            # Set new password and update
            user.set_password(new_password)
            self.user_repository.update(user)
            
            self.logger.info(f"Password reset for user: {user.username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error resetting password for user ID {user_id}: {e}")
            raise
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
        try:
            # Check if user exists
            user = self.user_repository.get_by_id(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            
            # Don't allow deletion of admin user (ID 1)
            if user_id == 1:
                raise ValueError("Cannot delete the default administrator user")
            
            # Perform delete
            result = self.user_repository.delete(user_id)
            if result:
                self.logger.info(f"Deleted user with ID: {user_id}")
            else:
                self.logger.warning(f"Failed to delete user with ID: {user_id}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error deleting user with ID {user_id}: {e}")
            raise
    
    def get_all_roles(self) -> List[Role]:
        """Get all user roles."""
        try:
            roles = self.role_repository.get_all()
            self.logger.info(f"Retrieved {len(roles)} roles")
            return roles
        except Exception as e:
            self.logger.error(f"Error getting all roles: {e}")
            raise
    
    def get_role_by_id(self, role_id: int) -> Optional[Role]:
        """Get role by ID."""
        try:
            role = self.role_repository.get_by_id(role_id)
            if role:
                self.logger.info(f"Retrieved role: {role}")
            else:
                self.logger.warning(f"Role not found with ID: {role_id}")
            return role
        except Exception as e:
            self.logger.error(f"Error getting role by ID {role_id}: {e}")
            raise
