"""
Main controller for home page and navigation.
"""

import cherrypy
import logging
from web.controllers.auth_controller import AuthController


class MainController:
    """Main application controller."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.auth = AuthController()
    
    @cherrypy.expose
    def index(self):
        """Home page."""
        # Check authentication
        self.auth.require_auth()
        
        username = cherrypy.session.get('username', 'Unknown')
        is_admin = cherrypy.session.get('is_admin', False)
        user_role = "Administrator" if is_admin else "Standard User"
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MyCRM - Dashboard</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f5f5f5;
                }}
                .header {{
                    background-color: #007bff;
                    color: white;
                    padding: 15px 30px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}
                .header h1 {{
                    margin: 0;
                }}
                .user-info {{
                    font-size: 14px;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 30px auto;
                    padding: 0 20px;
                }}
                .nav {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    margin-bottom: 30px;
                }}
                .nav-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                }}
                .nav-item {{
                    display: block;
                    padding: 20px;
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 6px;
                    text-decoration: none;
                    color: #333;
                    transition: background-color 0.2s;
                }}
                .nav-item:hover {{
                    background-color: #e9ecef;
                }}
                .nav-item h3 {{
                    margin: 0 0 10px 0;
                    color: #007bff;
                }}
                .nav-item p {{
                    margin: 0;
                    color: #666;
                    font-size: 14px;
                }}
                .stats {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .logout {{
                    color: white;
                    text-decoration: none;
                    padding: 8px 16px;
                    background-color: rgba(255,255,255,0.2);
                    border-radius: 4px;
                }}
                .logout:hover {{
                    background-color: rgba(255,255,255,0.3);
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>MyCRM Dashboard</h1>
                <div class="user-info">
                    Welcome, {username} ({user_role}) | 
                    <a href="/auth/logout" class="logout">Logout</a>
                </div>
            </div>
            
            <div class="container">
                <div class="nav">
                    <h2>Quick Actions</h2>
                    <div class="nav-grid">
                        <a href="/customers" class="nav-item">
                            <h3>Customer Management</h3>
                            <p>View, add, edit, and manage customer information</p>
                        </a>
                        
                        {'''
                        <a href="/email" class="nav-item">
                            <h3>Email Generation</h3>
                            <p>Create AI-powered personalized emails for customers</p>
                        </a>
                        ''' if is_admin else ''}
                        
                        {'''
                        <a href="/users" class="nav-item">
                            <h3>User Management</h3>
                            <p>Manage user accounts and permissions</p>
                        </a>
                        ''' if is_admin else ''}
                        
                        <a href="/email/logs" class="nav-item">
                            <h3>Email History</h3>
                            <p>View sent emails and email generation history</p>
                        </a>
                    </div>
                </div>
                
                <div class="stats">
                    <h2>System Information</h2>
                    <p><strong>Environment:</strong> Development Mode</p>
                    <p><strong>Data Source:</strong> Mock Data (SQL Server fallback active)</p>
                    <p><strong>AI Service:</strong> {"Enabled" if self._check_openai_status() else "Disabled"}</p>
                    <p><strong>Version:</strong> MyCRM v1.0.0</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _check_openai_status(self):
        """Check if OpenAI is configured."""
        from config.settings import get_openai_config
        config = get_openai_config()
        return bool(config.get('api_key'))
