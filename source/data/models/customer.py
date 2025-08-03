"""
Customer data model.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Customer:
    """Customer data model."""
    
    customer_id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    company_name: str = ""
    title: str = ""
    email: str = ""
    linkedin_url: str = ""
    is_active: bool = True
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    
    @property
    def full_name(self) -> str:
        """Get the customer's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def __str__(self) -> str:
        """String representation of the customer."""
        return f"{self.full_name} ({self.company_name})"
    
    def to_dict(self) -> dict:
        """Convert customer to dictionary."""
        return {
            'customer_id': self.customer_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'company_name': self.company_name,
            'title': self.title,
            'email': self.email,
            'linkedin_url': self.linkedin_url,
            'is_active': self.is_active,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'modified_date': self.modified_date.isoformat() if self.modified_date else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Customer':
        """Create customer from dictionary."""
        return cls(
            customer_id=data.get('customer_id'),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            company_name=data.get('company_name', ''),
            title=data.get('title', ''),
            email=data.get('email', ''),
            linkedin_url=data.get('linkedin_url', ''),
            is_active=data.get('is_active', True),
            created_date=datetime.fromisoformat(data['created_date']) if data.get('created_date') else None,
            modified_date=datetime.fromisoformat(data['modified_date']) if data.get('modified_date') else None
        )
    
    def validate(self) -> list[str]:
        """Validate customer data and return list of errors."""
        errors = []
        
        if not self.first_name.strip():
            errors.append("First name is required")
        
        if not self.last_name.strip():
            errors.append("Last name is required")
        
        if not self.email.strip():
            errors.append("Email is required")
        elif '@' not in self.email or '.' not in self.email.split('@')[-1]:
            errors.append("Email format is invalid")
        
        if self.linkedin_url and not (
            self.linkedin_url.startswith('http://') or 
            self.linkedin_url.startswith('https://')
        ):
            errors.append("LinkedIn URL must start with http:// or https://")
        
        return errors
