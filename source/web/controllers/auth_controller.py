"""
Authentication controller for login/logout functionality.
"""

import cherrypy
import logging
from business.services.user_service import UserService


class AuthController:
    """Controller for user authentication."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.user_service = UserService()
    
    @cherrypy.expose
    def index(self):
        """Redirect to login page."""
        raise cherrypy.HTTPRedirect('/auth/login')
    
    @cherrypy.expose
    def login(self, username=None, password=None, error_message=None):
        """Login page and authentication."""
        if cherrypy.request.method == 'GET':
            # Show login form
            return self._render_login_page(error_message)
        
        elif cherrypy.request.method == 'POST':
            try:
                if not username or not password:
                    raise cherrypy.HTTPRedirect('/auth/login?error_message=Username and password are required')
                
                # Authenticate user
                user = self.user_service.authenticate_user(username, password)
                if user:
                    # Set session
                    cherrypy.session['user_id'] = user.user_id
                    cherrypy.session['username'] = user.username
                    cherrypy.session['is_admin'] = user.is_admin
                    cherrypy.session['authenticated'] = True
                    
                    self.logger.info(f"User logged in: {username}")
                    raise cherrypy.HTTPRedirect('/')
                else:
                    raise cherrypy.HTTPRedirect('/auth/login?error_message=Invalid username or password')
                    
            except cherrypy.HTTPRedirect:
                # Re-raise HTTPRedirect - this is not an error, it's the normal flow
                raise
            except Exception as e:
                self.logger.error(f"Login error: {e}")
                raise cherrypy.HTTPRedirect('/auth/login?error_message=Login failed. Please try again.')
    
    @cherrypy.expose
    def logout(self):
        """Logout and clear session."""
        username = cherrypy.session.get('username', 'Unknown')
        cherrypy.session.clear()
        self.logger.info(f"User logged out: {username}")
        raise cherrypy.HTTPRedirect('/auth/login?error_message=You have been logged out')
    
    def _render_login_page(self, error_message=None):
        """Render the login page."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MyCRM - Login</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 400px;
                    margin: 100px auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .login-container {{
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .form-group {{
                    margin-bottom: 20px;
                }}
                label {{
                    display: block;
                    margin-bottom: 5px;
                    font-weight: bold;
                }}
                input[type="text"], input[type="password"] {{
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    box-sizing: border-box;
                }}
                button {{
                    width: 100%;
                    padding: 12px;
                    background-color: #007bff;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 16px;
                }}
                button:hover {{
                    background-color: #0056b3;
                }}
                .error {{
                    color: red;
                    margin-bottom: 15px;
                    padding: 10px;
                    background-color: #f8d7da;
                    border: 1px solid #f5c6cb;
                    border-radius: 4px;
                }}
                .info {{
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #d1ecf1;
                    border: 1px solid #bee5eb;
                    border-radius: 4px;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="login-container">
                <h2>MyCRM Login</h2>
                
                {f'<div class="error">{error_message}</div>' if error_message else ''}
                
                <form method="post" action="/auth/login">
                    <div class="form-group">
                        <label for="username">Username:</label>
                        <input type="text" id="username" name="username" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="password">Password:</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    
                    <button type="submit">Login</button>
                </form>
                
                <div class="info">
                    <strong>Default Accounts:</strong><br>
                    Administrator: admin / admin123<br>
                    Standard User: user / user123
                </div>
            </div>
        </body>
        </html>
        """
    
    def require_auth(self):
        """Check if user is authenticated."""
        if not cherrypy.session.get('authenticated', False):
            raise cherrypy.HTTPRedirect('/auth/login?error_message=Please log in to access this page')
    
    def require_admin(self):
        """Check if user is authenticated and is an admin."""
        self.require_auth()
        if not cherrypy.session.get('is_admin', False):
            raise cherrypy.HTTPError(403, "Access denied. Administrator privileges required.")
