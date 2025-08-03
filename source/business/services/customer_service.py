"""
Customer service for business logic operations.
"""

import logging
from typing import List, Optional
from data.factory import repository_factory
from data.models.customer import Customer


class CustomerService:
    """Service class for customer business logic."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.customer_repository = repository_factory.get_customer_repository()
    
    def get_all_customers(self) -> List[Customer]:
        """Get all customers."""
        try:
            customers = self.customer_repository.get_all()
            self.logger.info(f"Retrieved {len(customers)} customers")
            return customers
        except Exception as e:
            self.logger.error(f"Error getting all customers: {e}")
            raise
    
    def get_active_customers(self) -> List[Customer]:
        """Get all active customers."""
        try:
            customers = self.customer_repository.get_active_customers()
            self.logger.info(f"Retrieved {len(customers)} active customers")
            return customers
        except Exception as e:
            self.logger.error(f"Error getting active customers: {e}")
            raise
    
    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        """Get customer by ID."""
        try:
            customer = self.customer_repository.get_by_id(customer_id)
            if customer:
                self.logger.info(f"Retrieved customer: {customer}")
            else:
                self.logger.warning(f"Customer not found with ID: {customer_id}")
            return customer
        except Exception as e:
            self.logger.error(f"Error getting customer by ID {customer_id}: {e}")
            raise
    
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email address."""
        try:
            customer = self.customer_repository.get_by_email(email)
            if customer:
                self.logger.info(f"Retrieved customer by email: {customer}")
            else:
                self.logger.warning(f"Customer not found with email: {email}")
            return customer
        except Exception as e:
            self.logger.error(f"Error getting customer by email {email}: {e}")
            raise
    
    def create_customer(self, customer: Customer) -> Customer:
        """Create a new customer."""
        try:
            # Validate customer data
            errors = customer.validate()
            if errors:
                raise ValueError(f"Customer validation failed: {', '.join(errors)}")
            
            # Check for duplicate email
            existing_customer = self.customer_repository.get_by_email(customer.email)
            if existing_customer:
                raise ValueError(f"Customer with email {customer.email} already exists")
            
            # Create customer
            created_customer = self.customer_repository.create(customer)
            self.logger.info(f"Created customer: {created_customer}")
            return created_customer
            
        except Exception as e:
            self.logger.error(f"Error creating customer: {e}")
            raise
    
    def update_customer(self, customer: Customer) -> Customer:
        """Update an existing customer."""
        try:
            # Validate customer data
            errors = customer.validate()
            if errors:
                raise ValueError(f"Customer validation failed: {', '.join(errors)}")
            
            # Check if customer exists
            existing_customer = self.customer_repository.get_by_id(customer.customer_id)
            if not existing_customer:
                raise ValueError(f"Customer with ID {customer.customer_id} not found")
            
            # Check for duplicate email (excluding current customer)
            email_customer = self.customer_repository.get_by_email(customer.email)
            if email_customer and email_customer.customer_id != customer.customer_id:
                raise ValueError(f"Another customer with email {customer.email} already exists")
            
            # Update customer
            updated_customer = self.customer_repository.update(customer)
            self.logger.info(f"Updated customer: {updated_customer}")
            return updated_customer
            
        except Exception as e:
            self.logger.error(f"Error updating customer: {e}")
            raise
    
    def delete_customer(self, customer_id: int) -> bool:
        """Soft delete a customer (set is_active = False)."""
        try:
            # Check if customer exists
            customer = self.customer_repository.get_by_id(customer_id)
            if not customer:
                raise ValueError(f"Customer with ID {customer_id} not found")
            
            # Perform soft delete
            result = self.customer_repository.soft_delete(customer_id)
            if result:
                self.logger.info(f"Soft deleted customer with ID: {customer_id}")
            else:
                self.logger.warning(f"Failed to soft delete customer with ID: {customer_id}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error deleting customer with ID {customer_id}: {e}")
            raise
    
    def hard_delete_customer(self, customer_id: int) -> bool:
        """Hard delete a customer (permanent removal)."""
        try:
            # Check if customer exists
            customer = self.customer_repository.get_by_id(customer_id)
            if not customer:
                raise ValueError(f"Customer with ID {customer_id} not found")
            
            # Perform hard delete
            result = self.customer_repository.delete(customer_id)
            if result:
                self.logger.info(f"Hard deleted customer with ID: {customer_id}")
            else:
                self.logger.warning(f"Failed to hard delete customer with ID: {customer_id}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error hard deleting customer with ID {customer_id}: {e}")
            raise
    
    def search_customers(self, search_term: str) -> List[Customer]:
        """Search customers by name, company, or email."""
        try:
            all_customers = self.customer_repository.get_all()
            search_term = search_term.lower()
            
            matching_customers = []
            for customer in all_customers:
                if (search_term in customer.first_name.lower() or
                    search_term in customer.last_name.lower() or
                    search_term in customer.company_name.lower() or
                    search_term in customer.email.lower()):
                    matching_customers.append(customer)
            
            self.logger.info(f"Found {len(matching_customers)} customers matching '{search_term}'")
            return matching_customers
            
        except Exception as e:
            self.logger.error(f"Error searching customers with term '{search_term}': {e}")
            raise
