"""
Email log data model.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class EmailLog:
    """Email log data model."""
    
    email_log_id: Optional[int] = None
    customer_id: int = 0
    user_id: int = 0
    template_text: str = ""
    generated_email: str = ""
    recipient_email: str = ""
    subject: str = ""
    hipaa_compliance_check: str = ""
    ai_compliance_check: str = ""
    compliance_approved: bool = False
    email_sent: bool = False
    sent_date: Optional[datetime] = None
    created_date: Optional[datetime] = None
    
    def __str__(self) -> str:
        """String representation of the email log."""
        status = "Sent" if self.email_sent else "Draft"
        return f"Email to {self.recipient_email} - {status}"
    
    def to_dict(self) -> dict:
        """Convert email log to dictionary."""
        return {
            'email_log_id': self.email_log_id,
            'customer_id': self.customer_id,
            'user_id': self.user_id,
            'template_text': self.template_text,
            'generated_email': self.generated_email,
            'recipient_email': self.recipient_email,
            'subject': self.subject,
            'hipaa_compliance_check': self.hipaa_compliance_check,
            'ai_compliance_check': self.ai_compliance_check,
            'compliance_approved': self.compliance_approved,
            'email_sent': self.email_sent,
            'sent_date': self.sent_date.isoformat() if self.sent_date else None,
            'created_date': self.created_date.isoformat() if self.created_date else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'EmailLog':
        """Create email log from dictionary."""
        return cls(
            email_log_id=data.get('email_log_id'),
            customer_id=data.get('customer_id', 0),
            user_id=data.get('user_id', 0),
            template_text=data.get('template_text', ''),
            generated_email=data.get('generated_email', ''),
            recipient_email=data.get('recipient_email', ''),
            subject=data.get('subject', ''),
            hipaa_compliance_check=data.get('hipaa_compliance_check', ''),
            ai_compliance_check=data.get('ai_compliance_check', ''),
            compliance_approved=data.get('compliance_approved', False),
            email_sent=data.get('email_sent', False),
            sent_date=datetime.fromisoformat(data['sent_date']) if data.get('sent_date') else None,
            created_date=datetime.fromisoformat(data['created_date']) if data.get('created_date') else None
        )
    
    def validate(self) -> list[str]:
        """Validate email log data and return list of errors."""
        errors = []
        
        if self.customer_id <= 0:
            errors.append("Customer ID is required")
        
        if self.user_id <= 0:
            errors.append("User ID is required")
        
        if not self.template_text.strip():
            errors.append("Template text is required")
        
        if len(self.template_text) > 1000:
            errors.append("Template text cannot exceed 1000 characters")
        
        if not self.recipient_email.strip():
            errors.append("Recipient email is required")
        elif '@' not in self.recipient_email or '.' not in self.recipient_email.split('@')[-1]:
            errors.append("Recipient email format is invalid")
        
        return errors
