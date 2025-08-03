"""
User controller for user management operations.
"""

import cherrypy
import logging
from business.services.user_service import UserService
from data.models.user import User
from web.controllers.auth_controller import AuthController


class UserController:
    """Controller for user management."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.user_service = UserService()
        self.auth = AuthController()
    
    @cherrypy.expose
    def index(self):
        """User list page."""
        self.auth.require_admin()
        
        try:
            users = self.user_service.get_all_users()
            roles = self.user_service.get_all_roles()
            return self._render_user_list(users, roles)
        except Exception as e:
            self.logger.error(f"Error loading users: {e}")
            return self._render_error_page("Failed to load users", str(e))
    
    @cherrypy.expose
    def add(self, **kwargs):
        """Add new user."""
        self.auth.require_admin()
        
        if cherrypy.request.method == 'GET':
            roles = self.user_service.get_all_roles()
            return self._render_user_form(roles=roles)
        
        elif cherrypy.request.method == 'POST':
            try:
                user = User(
                    username=kwargs.get('username', ''),
                    email=kwargs.get('email', ''),
                    first_name=kwargs.get('first_name', ''),
                    last_name=kwargs.get('last_name', ''),
                    role_id=int(kwargs.get('role_id', 2))
                )
                
                password = kwargs.get('password', '')
                confirm_password = kwargs.get('confirm_password', '')
                
                if password != confirm_password:
                    raise ValueError("Passwords do not match")
                
                created_user = self.user_service.create_user(user, password)
                raise cherrypy.HTTPRedirect(f'/users/view/{created_user.user_id}')
                
            except Exception as e:
                self.logger.error(f"Error creating user: {e}")
                roles = self.user_service.get_all_roles()
                return self._render_user_form(data=kwargs, error=str(e), roles=roles)
    
    @cherrypy.expose
    def edit(self, user_id, **kwargs):
        """Edit existing user."""
        self.auth.require_admin()
        
        try:
            user_id = int(user_id)
            existing_user = self.user_service.get_user_by_id(user_id)
            
            if not existing_user:
                return self._render_error_page("User Not Found", f"User with ID {user_id} not found")
            
            if cherrypy.request.method == 'GET':
                roles = self.user_service.get_all_roles()
                return self._render_user_form(data=existing_user.to_dict(), edit_mode=True, roles=roles)
            
            elif cherrypy.request.method == 'POST':
                try:
                    updated_user = User(
                        user_id=user_id,
                        username=kwargs.get('username', ''),
                        email=kwargs.get('email', ''),
                        first_name=kwargs.get('first_name', ''),
                        last_name=kwargs.get('last_name', ''),
                        role_id=int(kwargs.get('role_id', 2)),
                        password_hash=existing_user.password_hash,
                        is_active=existing_user.is_active,
                        created_date=existing_user.created_date,
                        last_login_date=existing_user.last_login_date
                    )
                    
                    self.user_service.update_user(updated_user)
                    raise cherrypy.HTTPRedirect(f'/users/view/{user_id}')
                    
                except Exception as e:
                    self.logger.error(f"Error updating user: {e}")
                    roles = self.user_service.get_all_roles()
                    return self._render_user_form(data=kwargs, error=str(e), edit_mode=True, roles=roles)
                    
        except ValueError:
            return self._render_error_page("Invalid Request", "Invalid user ID")
    
    @cherrypy.expose
    def view(self, user_id):
        """View user details."""
        self.auth.require_admin()
        
        try:
            user_id = int(user_id)
            user = self.user_service.get_user_by_id(user_id)
            
            if not user:
                return self._render_error_page("User Not Found", f"User with ID {user_id} not found")
            
            role = self.user_service.get_role_by_id(user.role_id)
            return self._render_user_details(user, role)
            
        except ValueError:
            return self._render_error_page("Invalid Request", "Invalid user ID")
        except Exception as e:
            self.logger.error(f"Error viewing user: {e}")
            return self._render_error_page("Error", str(e))
    
    @cherrypy.expose
    def reset_password(self, user_id, **kwargs):
        """Reset user password."""
        self.auth.require_admin()
        
        try:
            user_id = int(user_id)
            user = self.user_service.get_user_by_id(user_id)
            
            if not user:
                return self._render_error_page("User Not Found", f"User with ID {user_id} not found")
            
            if cherrypy.request.method == 'GET':
                return self._render_password_reset_form(user)
            
            elif cherrypy.request.method == 'POST':
                try:
                    new_password = kwargs.get('new_password', '')
                    confirm_password = kwargs.get('confirm_password', '')
                    
                    if new_password != confirm_password:
                        raise ValueError("Passwords do not match")
                    
                    self.user_service.reset_password(user_id, new_password)
                    raise cherrypy.HTTPRedirect(f'/users/view/{user_id}?message=Password reset successfully')
                    
                except Exception as e:
                    self.logger.error(f"Error resetting password: {e}")
                    return self._render_password_reset_form(user, str(e))
                    
        except ValueError:
            return self._render_error_page("Invalid Request", "Invalid user ID")
    
    @cherrypy.expose
    def delete(self, user_id):
        """Delete user."""
        self.auth.require_admin()
        
        try:
            user_id = int(user_id)
            success = self.user_service.delete_user(user_id)
            
            if success:
                raise cherrypy.HTTPRedirect('/users?message=User deleted successfully')
            else:
                raise cherrypy.HTTPRedirect('/users?error=Failed to delete user')
                
        except ValueError:
            return self._render_error_page("Invalid Request", "Invalid user ID")
        except Exception as e:
            self.logger.error(f"Error deleting user: {e}")
            raise cherrypy.HTTPRedirect('/users?error=Failed to delete user')
    
    def _render_user_list(self, users, roles, message=None, error=None):
        """Render user list page."""
        role_dict = {role.role_id: role.role_name for role in roles}
        
        user_rows = ""
        for user in users:
            role_name = role_dict.get(user.role_id, "Unknown")
            status = "Active" if user.is_active else "Inactive"
            last_login = user.last_login_date.strftime('%Y-%m-%d %H:%M') if user.last_login_date else 'Never'
            
            user_rows += f"""
            <tr>
                <td>{user.user_id}</td>
                <td>{user.username}</td>
                <td>{user.full_name}</td>
                <td>{user.email}</td>
                <td>{role_name}</td>
                <td>{status}</td>
                <td>{last_login}</td>
                <td>
                    <a href="/users/view/{user.user_id}" class="btn btn-sm">View</a>
                    <a href="/users/edit/{user.user_id}" class="btn btn-sm btn-secondary">Edit</a>
                    <a href="/users/reset_password/{user.user_id}" class="btn btn-sm btn-warning">Reset Password</a>
                    {f'<a href="/users/delete/{user.user_id}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>' if user.user_id != 1 else ''}
                </td>
            </tr>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MyCRM - User Management</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f8f9fa; font-weight: bold; }}
                .btn {{ display: inline-block; padding: 6px 12px; text-decoration: none; background-color: #007bff; color: white; border-radius: 4px; margin-right: 5px; }}
                .btn:hover {{ background-color: #0056b3; }}
                .btn-secondary {{ background-color: #6c757d; }}
                .btn-secondary:hover {{ background-color: #545b62; }}
                .btn-warning {{ background-color: #ffc107; color: #212529; }}
                .btn-warning:hover {{ background-color: #e0a800; }}
                .btn-danger {{ background-color: #dc3545; }}
                .btn-danger:hover {{ background-color: #c82333; }}
                .btn-sm {{ padding: 4px 8px; font-size: 12px; }}
                .back-link {{ color: #007bff; text-decoration: none; }}
                .back-link:hover {{ text-decoration: underline; }}
                .message {{ color: green; margin-bottom: 15px; padding: 10px; background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 4px; }}
                .error {{ color: red; margin-bottom: 15px; padding: 10px; background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div>
                        <a href="/" class="back-link">← Back to Dashboard</a>
                        <h1>User Management</h1>
                    </div>
                    <a href="/users/add" class="btn">Add New User</a>
                </div>
                
                {f'<div class="message">{message}</div>' if message else ''}
                {f'<div class="error">{error}</div>' if error else ''}
                
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Username</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Status</th>
                            <th>Last Login</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {user_rows if user_rows else '<tr><td colspan="8">No users found</td></tr>'}
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """
    
    def _render_user_form(self, data=None, error=None, edit_mode=False, roles=None):
        """Render user add/edit form."""
        data = data or {}
        roles = roles or []
        title = "Edit User" if edit_mode else "Add New User"
        action = f"/users/edit/{data.get('user_id', '')}" if edit_mode else "/users/add"
        
        role_options = ""
        for role in roles:
            selected = "selected" if role.role_id == data.get('role_id') else ""
            role_options += f'<option value="{role.role_id}" {selected}>{role.role_name}</option>'
        
        password_fields = "" if edit_mode else """
            <div class="form-group">
                <label for="password">Password *:</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <div class="form-group">
                <label for="confirm_password">Confirm Password *:</label>
                <input type="password" id="confirm_password" name="confirm_password" required>
            </div>
        """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MyCRM - {title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .form-group {{ margin-bottom: 20px; }}
                label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
                input[type="text"], input[type="email"], input[type="password"], select {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }}
                .btn {{ padding: 12px 24px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; margin-right: 10px; }}
                .btn:hover {{ background-color: #0056b3; }}
                .btn-secondary {{ background-color: #6c757d; }}
                .btn-secondary:hover {{ background-color: #545b62; }}
                .error {{ color: red; margin-bottom: 15px; padding: 10px; background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 4px; }}
                .back-link {{ color: #007bff; text-decoration: none; }}
                .back-link:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/users" class="back-link">← Back to Users</a>
                <h1>{title}</h1>
                
                {f'<div class="error">{error}</div>' if error else ''}
                
                <form method="post" action="{action}">
                    <div class="form-group">
                        <label for="username">Username *:</label>
                        <input type="text" id="username" name="username" value="{data.get('username', '')}" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="email">Email *:</label>
                        <input type="email" id="email" name="email" value="{data.get('email', '')}" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="first_name">First Name *:</label>
                        <input type="text" id="first_name" name="first_name" value="{data.get('first_name', '')}" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="last_name">Last Name *:</label>
                        <input type="text" id="last_name" name="last_name" value="{data.get('last_name', '')}" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="role_id">Role *:</label>
                        <select id="role_id" name="role_id" required>
                            {role_options}
                        </select>
                    </div>
                    
                    {password_fields}
                    
                    <button type="submit" class="btn">{'Update' if edit_mode else 'Create'} User</button>
                    <a href="/users" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </body>
        </html>
        """
    
    def _render_user_details(self, user, role):
        """Render user details page."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MyCRM - User Details</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .detail-row {{ display: flex; margin-bottom: 15px; }}
                .detail-label {{ font-weight: bold; min-width: 150px; }}
                .detail-value {{ flex: 1; }}
                .btn {{ display: inline-block; padding: 10px 20px; text-decoration: none; background-color: #007bff; color: white; border-radius: 4px; margin-right: 10px; }}
                .btn:hover {{ background-color: #0056b3; }}
                .btn-secondary {{ background-color: #6c757d; }}
                .btn-secondary:hover {{ background-color: #545b62; }}
                .btn-warning {{ background-color: #ffc107; color: #212529; }}
                .btn-warning:hover {{ background-color: #e0a800; }}
                .btn-danger {{ background-color: #dc3545; }}
                .btn-danger:hover {{ background-color: #c82333; }}
                .back-link {{ color: #007bff; text-decoration: none; }}
                .back-link:hover {{ text-decoration: underline; }}
                .actions {{ margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/users" class="back-link">← Back to Users</a>
                <h1>User Details</h1>
                
                <div class="detail-row">
                    <div class="detail-label">ID:</div>
                    <div class="detail-value">{user.user_id}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Username:</div>
                    <div class="detail-value">{user.username}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Name:</div>
                    <div class="detail-value">{user.full_name}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Email:</div>
                    <div class="detail-value"><a href="mailto:{user.email}">{user.email}</a></div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Role:</div>
                    <div class="detail-value">{role.role_name if role else 'Unknown'}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Status:</div>
                    <div class="detail-value">{'Active' if user.is_active else 'Inactive'}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Created:</div>
                    <div class="detail-value">{user.created_date.strftime('%Y-%m-%d %H:%M') if user.created_date else 'Unknown'}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Last Login:</div>
                    <div class="detail-value">{user.last_login_date.strftime('%Y-%m-%d %H:%M') if user.last_login_date else 'Never'}</div>
                </div>
                
                <div class="actions">
                    <a href="/users/edit/{user.user_id}" class="btn btn-secondary">Edit User</a>
                    <a href="/users/reset_password/{user.user_id}" class="btn btn-warning">Reset Password</a>
                    {f'<a href="/users/delete/{user.user_id}" class="btn btn-danger" onclick="return confirm(\'Are you sure?\')">Delete User</a>' if user.user_id != 1 else ''}
                </div>
            </div>
        </body>
        </html>
        """
    
    def _render_password_reset_form(self, user, error=None):
        """Render password reset form."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MyCRM - Reset Password</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .user-info {{ background-color: #f8f9fa; padding: 20px; border-radius: 6px; margin-bottom: 20px; }}
                .form-group {{ margin-bottom: 20px; }}
                label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
                input[type="password"] {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }}
                .btn {{ padding: 12px 24px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; margin-right: 10px; }}
                .btn:hover {{ background-color: #0056b3; }}
                .btn-secondary {{ background-color: #6c757d; }}
                .btn-secondary:hover {{ background-color: #545b62; }}
                .error {{ color: red; margin-bottom: 15px; padding: 10px; background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 4px; }}
                .back-link {{ color: #007bff; text-decoration: none; }}
                .back-link:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/users/view/{user.user_id}" class="back-link">← Back to User Details</a>
                <h1>Reset Password</h1>
                
                <div class="user-info">
                    <h3>User: {user.full_name} ({user.username})</h3>
                    <p>Email: {user.email}</p>
                </div>
                
                {f'<div class="error">{error}</div>' if error else ''}
                
                <form method="post" action="/users/reset_password/{user.user_id}">
                    <div class="form-group">
                        <label for="new_password">New Password *:</label>
                        <input type="password" id="new_password" name="new_password" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="confirm_password">Confirm Password *:</label>
                        <input type="password" id="confirm_password" name="confirm_password" required>
                    </div>
                    
                    <button type="submit" class="btn">Reset Password</button>
                    <a href="/users/view/{user.user_id}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </body>
        </html>
        """
    
    def _render_error_page(self, title, message):
        """Render error page."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MyCRM - Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
                .error {{ color: #dc3545; }}
                .back-link {{ color: #007bff; text-decoration: none; }}
                .back-link:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="error">{title}</h1>
                <p>{message}</p>
                <p><a href="/users" class="back-link">← Back to Users</a></p>
            </div>
        </body>
        </html>
        """
