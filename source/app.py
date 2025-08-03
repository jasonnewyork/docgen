#!/usr/bin/env python3
"""
MyCRM Application Entry Point
A Customer Relationship Management system with AI-powered email generation.
"""

import os
import sys
import cherrypy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web.controllers.main_controller import MainController
from web.controllers.customer_controller import CustomerController
from web.controllers.email_controller import EmailController
from web.controllers.user_controller import UserController
from web.controllers.auth_controller import AuthController
from config.settings import get_cherrypy_config


class MyCRMApp:
    """Main application class for MyCRM."""
    
    def __init__(self):
        self.setup_logging()
        self.setup_routes()
    
    def setup_logging(self):
        """Configure application logging."""
        import logging
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/mycrm.log'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("MyCRM Application starting...")
    
    def setup_routes(self):
        """Set up URL routing for the application."""
        # Mount controllers
        cherrypy.tree.mount(MainController(), '/')
        cherrypy.tree.mount(CustomerController(), '/customers')
        cherrypy.tree.mount(EmailController(), '/email')
        cherrypy.tree.mount(UserController(), '/users')
        cherrypy.tree.mount(AuthController(), '/auth')
    
    def run(self):
        """Start the CherryPy server."""
        try:
            config = get_cherrypy_config()
            cherrypy.config.update(config)
            
            self.logger.info("Starting CherryPy server on http://localhost:8080")
            cherrypy.engine.start()
            cherrypy.engine.block()
            
        except KeyboardInterrupt:
            self.logger.info("Shutting down MyCRM Application...")
            cherrypy.engine.exit()
        except Exception as e:
            self.logger.error(f"Error starting application: {e}")
            raise


if __name__ == '__main__':
    app = MyCRMApp()
    app.run()
