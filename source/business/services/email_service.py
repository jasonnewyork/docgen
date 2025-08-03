"""
Email service for AI-powered email generation and sending.
"""

import logging
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict, Any
import openai
from config.settings import get_openai_config, get_email_config, get_security_config
from data.factory import repository_factory
from data.models.customer import Customer
from data.models.email_log import EmailLog


class EmailService:
    """Service class for AI-powered email generation and sending."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.email_log_repository = repository_factory.get_email_log_repository()
        self.openai_config = get_openai_config()
        self.email_config = get_email_config()
        self.security_config = get_security_config()
        
        # Initialize OpenAI client
        if self.openai_config['api_key']:
            openai.api_key = self.openai_config['api_key']
        else:
            self.logger.warning("OpenAI API key not configured")
    
    def generate_personalized_email(self, customer: Customer, template_text: str, user_id: int) -> EmailLog:
        """Generate a personalized email using AI."""
        try:
            # Create email log entry
            email_log = EmailLog(
                customer_id=customer.customer_id,
                user_id=user_id,
                template_text=template_text,
                recipient_email=customer.email
            )
            
            # Generate personalized email content using OpenAI
            if self.openai_config['api_key']:
                email_log.generated_email = self._generate_with_openai(customer, template_text)
                email_log.subject = self._generate_subject_with_openai(customer, template_text)
            else:
                # Fallback to simple template substitution
                email_log.generated_email = self._generate_fallback_email(customer, template_text)
                email_log.subject = f"Message from MyCRM - {customer.company_name}"
            
            # Perform compliance checks
            self._perform_compliance_checks(email_log)
            
            # Save email log
            saved_log = self.email_log_repository.create(email_log)
            self.logger.info(f"Generated personalized email for customer: {customer}")
            
            return saved_log
            
        except Exception as e:
            self.logger.error(f"Error generating personalized email: {e}")
            raise

    def generate_bulk_personalized_emails(self, customers: List[Customer], template_text: str, user_id: int) -> List[EmailLog]:
        """Generate personalized emails for multiple customers using AI."""
        try:
            email_logs = []
            
            for customer in customers:
                try:
                    email_log = self.generate_personalized_email(customer, template_text, user_id)
                    email_logs.append(email_log)
                    self.logger.info(f"Generated email for customer: {customer.full_name}")
                except Exception as e:
                    self.logger.error(f"Failed to generate email for customer {customer.full_name}: {e}")
                    # Create a failed email log entry
                    failed_log = EmailLog(
                        customer_id=customer.customer_id,
                        user_id=user_id,
                        template_text=template_text,
                        recipient_email=customer.email,
                        status='failed',
                        error_message=str(e)
                    )
                    email_logs.append(self.email_log_repository.create(failed_log))
            
            self.logger.info(f"Generated {len(email_logs)} emails for {len(customers)} customers")
            return email_logs
            
        except Exception as e:
            self.logger.error(f"Error generating bulk personalized emails: {e}")
            raise

    def send_bulk_emails(self, email_log_ids: List[int]) -> Dict[int, bool]:
        """Send multiple emails and return success status for each."""
        try:
            results = {}
            
            for email_log_id in email_log_ids:
                try:
                    success = self.send_email(email_log_id)
                    results[email_log_id] = success
                    self.logger.info(f"Email {email_log_id} send result: {success}")
                except Exception as e:
                    self.logger.error(f"Failed to send email {email_log_id}: {e}")
                    results[email_log_id] = False
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error sending bulk emails: {e}")
            raise
    
    def _generate_with_openai(self, customer: Customer, template_text: str) -> str:
        """Generate email content using OpenAI."""
        try:
            prompt = f"""
            Please personalize the following email template for a customer:
            
            Customer Information:
            - Name: {customer.full_name}
            - Company: {customer.company_name}
            - Title: {customer.title}
            
            Email Template:
            {template_text}
            
            Please create a professional, personalized email that:
            1. Uses the customer's name and company appropriately
            2. Maintains a professional tone
            3. Is appropriate for business communication
            4. Does not include any inappropriate content
            
            Return only the email body content, no subject line.
            """
            
            response = openai.chat.completions.create(
                model=self.openai_config['model'],
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional email assistant that creates personalized business emails."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=self.openai_config['max_tokens'],
                temperature=self.openai_config['temperature']
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating email with OpenAI: {e}")
            # Fallback to simple substitution
            return self._generate_fallback_email(customer, template_text)
    
    def _generate_subject_with_openai(self, customer: Customer, template_text: str) -> str:
        """Generate email subject using OpenAI."""
        try:
            prompt = f"""
            Based on this email template for {customer.full_name} at {customer.company_name}:
            {template_text[:200]}...
            
            Generate a professional email subject line that is:
            1. Clear and concise
            2. Relevant to the content
            3. Professional
            4. Under 50 characters
            
            Return only the subject line, no quotes or extra text.
            """
            
            response = openai.chat.completions.create(
                model=self.openai_config['model'],
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional email assistant that creates email subject lines."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=50,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating subject with OpenAI: {e}")
            return f"Message for {customer.company_name}"
    
    def _generate_fallback_email(self, customer: Customer, template_text: str) -> str:
        """Generate email using simple template substitution."""
        personalized_text = template_text
        
        # Simple substitutions
        personalized_text = personalized_text.replace("{name}", customer.full_name)
        personalized_text = personalized_text.replace("{first_name}", customer.first_name)
        personalized_text = personalized_text.replace("{last_name}", customer.last_name)
        personalized_text = personalized_text.replace("{company}", customer.company_name)
        personalized_text = personalized_text.replace("{title}", customer.title)
        
        return f"Dear {customer.full_name},\n\n{personalized_text}\n\nBest regards,\nMyCRM Team"
    
    def _perform_compliance_checks(self, email_log: EmailLog):
        """Perform HIPAA and AI compliance checks."""
        compliance_approved = True
        
        # HIPAA compliance check
        if self.security_config['enable_hipaa_compliance']:
            email_log.hipaa_compliance_check = self._check_hipaa_compliance(email_log.generated_email)
            if "VIOLATION" in email_log.hipaa_compliance_check.upper():
                compliance_approved = False
        else:
            email_log.hipaa_compliance_check = "HIPAA compliance checking disabled"
        
        # AI compliance check
        if self.security_config['enable_ai_compliance']:
            email_log.ai_compliance_check = self._check_ai_compliance(email_log.generated_email)
            if "VIOLATION" in email_log.ai_compliance_check.upper():
                compliance_approved = False
        else:
            email_log.ai_compliance_check = "AI compliance checking disabled"
        
        email_log.compliance_approved = compliance_approved
        
        self.logger.info(f"Compliance check completed - Approved: {compliance_approved}")
    
    def _check_hipaa_compliance(self, email_content: str) -> str:
        """Check email content for HIPAA compliance."""
        try:
            if not self.openai_config['api_key']:
                return "HIPAA compliance check skipped - OpenAI not configured"
            
            prompt = f"""
            Please review the following email content for HIPAA compliance:
            
            {email_content}
            
            Check for:
            1. No personal health information (PHI)
            2. No medical condition details
            3. No protected health information
            4. Professional business communication only
            
            Respond with either:
            "APPROVED: [brief reason]" or "VIOLATION: [specific issue]"
            """
            
            response = openai.chat.completions.create(
                model=self.openai_config['model'],
                messages=[
                    {
                        "role": "system",
                        "content": "You are a HIPAA compliance officer reviewing business emails."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=200,
                temperature=0.1
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error checking HIPAA compliance: {e}")
            return f"HIPAA compliance check failed: {str(e)}"
    
    def _check_ai_compliance(self, email_content: str) -> str:
        """Check email content for Microsoft Responsible AI principles."""
        try:
            if not self.openai_config['api_key']:
                return "AI compliance check skipped - OpenAI not configured"
            
            prompt = f"""
            Please review the following email content against Microsoft's Responsible AI principles:
            
            {email_content}
            
            Check for:
            1. Fairness and inclusivity
            2. Reliability and safety
            3. Privacy and security
            4. Transparency
            5. Accountability
            6. No harmful or inappropriate content
            
            Respond with either:
            "APPROVED: [brief reason]" or "VIOLATION: [specific issue]"
            """
            
            response = openai.chat.completions.create(
                model=self.openai_config['model'],
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI ethics reviewer checking content for responsible AI principles."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=200,
                temperature=0.1
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error checking AI compliance: {e}")
            return f"AI compliance check failed: {str(e)}"
    
    def send_email(self, email_log_id: int) -> bool:
        """Send an email that has been generated and approved."""
        try:
            # Get email log
            email_log = self.email_log_repository.get_by_id(email_log_id)
            if not email_log:
                raise ValueError(f"Email log with ID {email_log_id} not found")
            
            # Check compliance approval
            if not email_log.compliance_approved:
                raise ValueError("Email has not been approved for sending due to compliance issues")
            
            # Check if already sent
            if email_log.email_sent:
                raise ValueError("Email has already been sent")
            
            # Send email
            success = self._send_smtp_email(
                email_log.recipient_email,
                email_log.subject,
                email_log.generated_email
            )
            
            if success:
                # Update email log
                email_log.email_sent = True
                email_log.sent_date = datetime.now()
                self.email_log_repository.update(email_log)
                
                self.logger.info(f"Email sent successfully to: {email_log.recipient_email}")
                return True
            else:
                self.logger.error(f"Failed to send email to: {email_log.recipient_email}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            raise
    
    def _send_smtp_email(self, recipient: str, subject: str, body: str) -> bool:
        """Send email using SMTP."""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.email_config['sender_name']} <{self.email_config['sender_email']}>"
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Attach body
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to SMTP server and send
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                if self.email_config['use_tls']:
                    server.starttls()
                
                if self.email_config['smtp_username'] and self.email_config['smtp_password']:
                    server.login(self.email_config['smtp_username'], self.email_config['smtp_password'])
                
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            self.logger.error(f"SMTP send error: {e}")
            return False
    
    def get_email_logs_by_customer(self, customer_id: int) -> List[EmailLog]:
        """Get all email logs for a specific customer."""
        try:
            logs = self.email_log_repository.get_by_customer_id(customer_id)
            self.logger.info(f"Retrieved {len(logs)} email logs for customer ID: {customer_id}")
            return logs
        except Exception as e:
            self.logger.error(f"Error getting email logs for customer {customer_id}: {e}")
            raise
    
    def get_email_logs_by_user(self, user_id: int) -> List[EmailLog]:
        """Get all email logs created by a specific user."""
        try:
            logs = self.email_log_repository.get_by_user_id(user_id)
            self.logger.info(f"Retrieved {len(logs)} email logs for user ID: {user_id}")
            return logs
        except Exception as e:
            self.logger.error(f"Error getting email logs for user {user_id}: {e}")
            raise
    
    def get_all_sent_emails(self) -> List[EmailLog]:
        """Get all sent emails."""
        try:
            logs = self.email_log_repository.get_sent_emails()
            self.logger.info(f"Retrieved {len(logs)} sent emails")
            return logs
        except Exception as e:
            self.logger.error(f"Error getting sent emails: {e}")
            raise
