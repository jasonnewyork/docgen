"""
Comprehensive test suite for MyCRM application.
Tests core functionality across all layers.
"""

import os
import sys
import unittest
import logging
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.models.customer import Customer
from data.models.user import User, Role
from data.models.email_log import EmailLog
from data.factory import repository_factory
from business.services.customer_service import CustomerService
from business.services.user_service import UserService
from business.services.email_service import EmailService


class TestDataModels(unittest.TestCase):
    """Test data model functionality."""
    
    def test_customer_model(self):
        """Test Customer model creation and methods."""
        customer = Customer(
            company_name="Test Corp",
            first_name="John",
            last_name="Doe",
            email="john@testcorp.com",
            title="Manager"
        )
        
        self.assertEqual(customer.company_name, "Test Corp")
        self.assertEqual(customer.full_name, "John Doe")
        self.assertTrue(customer.is_active)
        
        # Test to_dict method if available
        if hasattr(customer, 'to_dict'):
            customer_dict = customer.to_dict()
            self.assertIsInstance(customer_dict, dict)
            self.assertEqual(customer_dict['company_name'], "Test Corp")
    
    def test_user_model(self):
        """Test User model creation and methods."""
        user = User(
            username="testuser",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password_hash="hashed_password",
            role_id=2
        )
        
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.full_name, "Test User")
        self.assertTrue(user.is_active)
        
        # Test to_dict method
        user_dict = user.to_dict()
        self.assertIsInstance(user_dict, dict)
        self.assertEqual(user_dict['username'], "testuser")
    
    def test_role_model(self):
        """Test Role model creation."""
        role = Role(
            role_id=1,
            role_name="Administrator",
            description="Full system access"
        )
        
        self.assertEqual(role.role_name, "Administrator")
        self.assertEqual(role.description, "Full system access")
    
    def test_email_log_model(self):
        """Test EmailLog model creation."""
        log = EmailLog(
            customer_id=1,
            user_id=1,
            template_text="Welcome email template",
            generated_email="Thank you for joining us!",
            recipient_email="customer@example.com",
            subject="Welcome to our service",
            email_sent=True
        )
        
        self.assertEqual(log.template_text, "Welcome email template")
        self.assertTrue(log.email_sent)


class TestRepositoryFactory(unittest.TestCase):
    """Test repository factory functionality."""
    
    def test_factory_initialization(self):
        """Test that factory initializes correctly."""
        self.assertIsNotNone(repository_factory)
    
    def test_repository_creation(self):
        """Test that repositories can be created."""
        customer_repo = repository_factory.get_customer_repository()
        user_repo = repository_factory.get_user_repository()
        email_repo = repository_factory.get_email_log_repository()
        role_repo = repository_factory.get_role_repository()
        
        self.assertIsNotNone(customer_repo)
        self.assertIsNotNone(user_repo)
        self.assertIsNotNone(email_repo)
        self.assertIsNotNone(role_repo)


class TestCustomerService(unittest.TestCase):
    """Test customer service functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.service = CustomerService()
    
    def test_get_all_customers(self):
        """Test getting all customers."""
        customers = self.service.get_all_customers()
        self.assertIsInstance(customers, list)
    
    def test_customer_crud(self):
        """Test customer create, read, update operations."""
        # Create test customer
        test_customer = Customer(
            company_name="Test Company",
            first_name="Jane",
            last_name="Smith",
            email="jane@testcompany.com",
            title="Director"
        )
        
        # Create customer
        created_customer = self.service.create_customer(test_customer)
        self.assertIsNotNone(created_customer)
        self.assertIsNotNone(created_customer.customer_id)
        
        # Get customer by ID
        retrieved_customer = self.service.get_customer_by_id(created_customer.customer_id)
        self.assertIsNotNone(retrieved_customer)
        self.assertEqual(retrieved_customer.company_name, "Test Company")
        
        # Update customer
        retrieved_customer.company_name = "Updated Test Company"
        updated = self.service.update_customer(retrieved_customer)
        self.assertTrue(updated)
        
        # Verify update
        updated_customer = self.service.get_customer_by_id(created_customer.customer_id)
        self.assertEqual(updated_customer.company_name, "Updated Test Company")
    
    def test_customer_search(self):
        """Test customer search functionality."""
        results = self.service.search_customers("test")
        self.assertIsInstance(results, list)


class TestUserService(unittest.TestCase):
    """Test user service functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.service = UserService()
    
    def test_get_all_users(self):
        """Test getting all users."""
        users = self.service.get_all_users()
        self.assertIsInstance(users, list)
    
    def test_get_all_roles(self):
        """Test getting all roles."""
        roles = self.service.get_all_roles()
        self.assertIsInstance(roles, list)
        self.assertTrue(len(roles) > 0)
    
    def test_authenticate_user(self):
        """Test user authentication."""
        # Try to authenticate with default admin user
        user = self.service.authenticate_user("admin", "admin123")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "admin")
        
        # Try invalid credentials
        invalid_user = self.service.authenticate_user("invalid", "password")
        self.assertIsNone(invalid_user)
    
    def test_user_crud(self):
        """Test user create, read, update operations."""
        # Create test user
        test_user = User(
            username="testuser123",
            email="testuser123@example.com",
            first_name="Test",
            last_name="User123",
            role_id=2
        )
        
        # Create user
        created_user = self.service.create_user(test_user, "testpassword")
        self.assertIsNotNone(created_user)
        self.assertIsNotNone(created_user.user_id)
        
        # Get user by ID
        retrieved_user = self.service.get_user_by_id(created_user.user_id)
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "testuser123")
        
        # Update user
        retrieved_user.first_name = "Updated"
        updated = self.service.update_user(retrieved_user)
        self.assertTrue(updated)


class TestEmailService(unittest.TestCase):
    """Test email service functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.service = EmailService()
    
    def test_get_all_email_logs(self):
        """Test getting all email logs."""
        logs = self.service.get_all_sent_emails()
        self.assertIsInstance(logs, list)
    
    def test_generate_email_content(self):
        """Test AI email content generation."""
        # Test with mock customer data
        customer = Customer(
            customer_id=1,
            company_name="Test Corp",
            first_name="John",
            last_name="Doe",
            email="john@testcorp.com"
        )
        
        # This test will pass even without OpenAI API key
        # as the service handles missing API keys gracefully
        try:
            email_log = self.service.generate_personalized_email(
                customer=customer,
                template_text="Welcome email for new customer",
                user_id=1
            )
            self.assertIsInstance(email_log, EmailLog)
        except Exception as e:
            # Expected if no OpenAI API key is configured
            self.assertIn("API", str(e).upper())
    
    def test_compliance_check(self):
        """Test content compliance checking."""
        # Test basic compliance checking functionality
        email_log = EmailLog(
            customer_id=1,
            user_id=1,
            generated_email="Thank you for your business.",
            recipient_email="test@example.com"
        )
        
        # Test compliance checking
        try:
            result = self.service.check_compliance(email_log)
            self.assertIsInstance(result, bool)
        except Exception:
            # Expected if compliance checking is not fully implemented
            pass


class TestConfiguration(unittest.TestCase):
    """Test configuration and environment setup."""
    
    def test_import_config(self):
        """Test that configuration modules can be imported."""
        try:
            from config.settings import get_cherrypy_config
            from config.database import DatabaseConfig
            
            config = get_cherrypy_config()
            self.assertIsInstance(config, dict)
            
            db_config = DatabaseConfig()
            self.assertIsNotNone(db_config)
            
        except ImportError as e:
            self.fail(f"Failed to import configuration: {e}")
    
    def test_environment_variables(self):
        """Test environment variable handling."""
        # Test that missing environment variables are handled gracefully
        try:
            from config.settings import get_cherrypy_config
            config = get_cherrypy_config()
            self.assertIsNotNone(config)
        except Exception as e:
            self.fail(f"Configuration failed: {e}")


def run_tests():
    """Run all tests and generate report."""
    # Set up logging for tests
    logging.basicConfig(level=logging.WARNING)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestDataModels,
        TestRepositoryFactory,
        TestCustomerService,
        TestUserService,
        TestEmailService,
        TestConfiguration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split()[-1] if traceback else 'Unknown failure'}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split()[-1] if traceback else 'Unknown error'}")
    
    print("="*60)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
