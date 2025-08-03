"""
User data model.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import bcrypt


@dataclass
class User:
    """User data model."""
    
    user_id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    role_id: int = 2  # Default to standard user
    is_active: bool = True
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    last_login_date: Optional[datetime] = None
    
    @property
    def full_name(self) -> str:
        """Get the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_admin(self) -> bool:
        """Check if user is an administrator."""
        return self.role_id == 1
    
    def set_password(self, password: str) -> None:
        """Set the user's password (hashed)."""
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Check if the provided password is correct."""
        if not self.password_hash:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def __str__(self) -> str:
        """String representation of the user."""
        return f"{self.username} ({self.full_name})"
    
    def to_dict(self, include_password=False) -> dict:
        """Convert user to dictionary."""
        data = {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role_id': self.role_id,
            'is_active': self.is_active,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'modified_date': self.modified_date.isoformat() if self.modified_date else None,
            'last_login_date': self.last_login_date.isoformat() if self.last_login_date else None
        }
        
        if include_password:
            data['password_hash'] = self.password_hash
        
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary."""
        return cls(
            user_id=data.get('user_id'),
            username=data.get('username', ''),
            password_hash=data.get('password_hash', ''),
            email=data.get('email', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            role_id=data.get('role_id', 2),
            is_active=data.get('is_active', True),
            created_date=datetime.fromisoformat(data['created_date']) if data.get('created_date') else None,
            modified_date=datetime.fromisoformat(data['modified_date']) if data.get('modified_date') else None,
            last_login_date=datetime.fromisoformat(data['last_login_date']) if data.get('last_login_date') else None
        )
    
    def validate(self) -> list[str]:
        """Validate user data and return list of errors."""
        errors = []
        
        if not self.username.strip():
            errors.append("Username is required")
        elif len(self.username.strip()) < 3:
            errors.append("Username must be at least 3 characters long")
        
        if not self.email.strip():
            errors.append("Email is required")
        elif '@' not in self.email or '.' not in self.email.split('@')[-1]:
            errors.append("Email format is invalid")
        
        if not self.first_name.strip():
            errors.append("First name is required")
        
        if not self.last_name.strip():
            errors.append("Last name is required")
        
        if self.role_id not in [1, 2]:
            errors.append("Invalid role ID")
        
        return errors


@dataclass
class Role:
    """User role data model."""
    
    role_id: int
    role_name: str
    description: str = ""
    
    def __str__(self) -> str:
        """String representation of the role."""
        return self.role_name
    
    def to_dict(self) -> dict:
        """Convert role to dictionary."""
        return {
            'role_id': self.role_id,
            'role_name': self.role_name,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Role':
        """Create role from dictionary."""
        return cls(
            role_id=data['role_id'],
            role_name=data['role_name'],
            description=data.get('description', '')
        )
