"""
Customer controller for customer management operations.
"""

import cherrypy
import logging
import json
from business.services.customer_service import CustomerService
from data.models.customer import Customer
from web.controllers.auth_controller import AuthController


class CustomerController:
    """Controller for customer management."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.customer_service = CustomerService()
        self.auth = AuthController()
    
    @cherrypy.expose
    def index(self):
        """Customer list page."""
        self.auth.require_auth()
        
        try:
            customers = self.customer_service.get_active_customers()
            return self._render_customer_list(customers)
        except Exception as e:
            self.logger.error(f"Error loading customers: {e}")
            return self._render_error_page("Failed to load customers", str(e))
    
    @cherrypy.expose
    def add(self, **kwargs):
        """Add new customer."""
        self.auth.require_admin()
        
        if cherrypy.request.method == 'GET':
            return self._render_customer_form()
        
        elif cherrypy.request.method == 'POST':
            try:
                customer = Customer(
                    first_name=kwargs.get('first_name', ''),
                    last_name=kwargs.get('last_name', ''),
                    company_name=kwargs.get('company_name', ''),
                    title=kwargs.get('title', ''),
                    email=kwargs.get('email', ''),
                    linkedin_url=kwargs.get('linkedin_url', '')
                )
                
                created_customer = self.customer_service.create_customer(customer)
                raise cherrypy.HTTPRedirect(f'/customers/view/{created_customer.customer_id}')
                
            except Exception as e:
                self.logger.error(f"Error creating customer: {e}")
                return self._render_customer_form(kwargs, str(e))
    
    @cherrypy.expose
    def edit(self, customer_id, **kwargs):
        """Edit existing customer."""
        self.auth.require_admin()
        
        try:
            customer_id = int(customer_id)
            existing_customer = self.customer_service.get_customer_by_id(customer_id)
            
            if not existing_customer:
                return self._render_error_page("Customer Not Found", f"Customer with ID {customer_id} not found")
            
            if cherrypy.request.method == 'GET':
                return self._render_customer_form(existing_customer.to_dict(), edit_mode=True)
            
            elif cherrypy.request.method == 'POST':
                try:
                    updated_customer = Customer(
                        customer_id=customer_id,
                        first_name=kwargs.get('first_name', ''),
                        last_name=kwargs.get('last_name', ''),
                        company_name=kwargs.get('company_name', ''),
                        title=kwargs.get('title', ''),
                        email=kwargs.get('email', ''),
                        linkedin_url=kwargs.get('linkedin_url', ''),
                        is_active=existing_customer.is_active,
                        created_date=existing_customer.created_date
                    )
                    
                    self.customer_service.update_customer(updated_customer)
                    raise cherrypy.HTTPRedirect(f'/customers/view/{customer_id}')
                    
                except Exception as e:
                    self.logger.error(f"Error updating customer: {e}")
                    return self._render_customer_form(kwargs, str(e), edit_mode=True)
                    
        except ValueError:
            return self._render_error_page("Invalid Request", "Invalid customer ID")
    
    @cherrypy.expose
    def view(self, customer_id):
        """View customer details."""
        self.auth.require_auth()
        
        try:
            customer_id = int(customer_id)
            customer = self.customer_service.get_customer_by_id(customer_id)
            
            if not customer:
                return self._render_error_page("Customer Not Found", f"Customer with ID {customer_id} not found")
            
            return self._render_customer_details(customer)
            
        except ValueError:
            return self._render_error_page("Invalid Request", "Invalid customer ID")
        except Exception as e:
            self.logger.error(f"Error viewing customer: {e}")
            return self._render_error_page("Error", str(e))
    
    @cherrypy.expose
    def delete(self, customer_id):
        """Delete customer (soft delete)."""
        self.auth.require_admin()
        
        try:
            customer_id = int(customer_id)
            success = self.customer_service.delete_customer(customer_id)
            
            if success:
                raise cherrypy.HTTPRedirect('/customers?message=Customer deleted successfully')
            else:
                raise cherrypy.HTTPRedirect('/customers?error=Failed to delete customer')
                
        except ValueError:
            return self._render_error_page("Invalid Request", "Invalid customer ID")
        except Exception as e:
            self.logger.error(f"Error deleting customer: {e}")
            raise cherrypy.HTTPRedirect('/customers?error=Failed to delete customer')
    
    def _render_customer_list(self, customers):
        """Render customer list page."""
        is_admin = cherrypy.session.get('is_admin', False)
        
        customer_rows = ""
        for customer in customers:
            customer_rows += f"""
            <tr>
                <td>{customer.customer_id}</td>
                <td>{customer.full_name}</td>
                <td>{customer.company_name}</td>
                <td>{customer.title}</td>
                <td>{customer.email}</td>
                <td>
                    <a href="/customers/view/{customer.customer_id}" class="btn btn-sm">View</a>
                    {f'<a href="/customers/edit/{customer.customer_id}" class="btn btn-sm btn-secondary">Edit</a>' if is_admin else ''}
                    {f'<a href="/customers/delete/{customer.customer_id}" class="btn btn-sm btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>' if is_admin else ''}
                </td>
            </tr>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MyCRM - Customers</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f8f9fa; font-weight: bold; }}
                .btn {{ display: inline-block; padding: 6px 12px; text-decoration: none; background-color: #007bff; color: white; border-radius: 4px; margin-right: 5px; }}
                .btn:hover {{ background-color: #0056b3; }}
                .btn-secondary {{ background-color: #6c757d; }}
                .btn-secondary:hover {{ background-color: #545b62; }}
                .btn-danger {{ background-color: #dc3545; }}
                .btn-danger:hover {{ background-color: #c82333; }}
                .btn-sm {{ padding: 4px 8px; font-size: 12px; }}
                .back-link {{ color: #007bff; text-decoration: none; }}
                .back-link:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div>
                        <a href="/" class="back-link">← Back to Dashboard</a>
                        <h1>Customer Management</h1>
                    </div>
                    {f'<a href="/customers/add" class="btn">Add New Customer</a>' if is_admin else ''}
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Company</th>
                            <th>Title</th>
                            <th>Email</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {customer_rows if customer_rows else '<tr><td colspan="6">No customers found</td></tr>'}
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """
    
    def _render_customer_form(self, data=None, error=None, edit_mode=False):
        """Render customer add/edit form."""
        data = data or {}
        title = "Edit Customer" if edit_mode else "Add New Customer"
        action = f"/customers/edit/{data.get('customer_id', '')}" if edit_mode else "/customers/add"
        
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
                input[type="text"], input[type="email"], input[type="url"] {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }}
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
                <a href="/customers" class="back-link">← Back to Customers</a>
                <h1>{title}</h1>
                
                {f'<div class="error">{error}</div>' if error else ''}
                
                <form method="post" action="{action}">
                    <div class="form-group">
                        <label for="first_name">First Name *:</label>
                        <input type="text" id="first_name" name="first_name" value="{data.get('first_name', '')}" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="last_name">Last Name *:</label>
                        <input type="text" id="last_name" name="last_name" value="{data.get('last_name', '')}" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="company_name">Company Name:</label>
                        <input type="text" id="company_name" name="company_name" value="{data.get('company_name', '')}">
                    </div>
                    
                    <div class="form-group">
                        <label for="title">Title:</label>
                        <input type="text" id="title" name="title" value="{data.get('title', '')}">
                    </div>
                    
                    <div class="form-group">
                        <label for="email">Email *:</label>
                        <input type="email" id="email" name="email" value="{data.get('email', '')}" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="linkedin_url">LinkedIn URL:</label>
                        <input type="url" id="linkedin_url" name="linkedin_url" value="{data.get('linkedin_url', '')}">
                    </div>
                    
                    <button type="submit" class="btn">{'Update' if edit_mode else 'Create'} Customer</button>
                    <a href="/customers" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </body>
        </html>
        """
    
    def _render_customer_details(self, customer):
        """Render customer details page."""
        is_admin = cherrypy.session.get('is_admin', False)
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MyCRM - Customer Details</title>
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
                .btn-danger {{ background-color: #dc3545; }}
                .btn-danger:hover {{ background-color: #c82333; }}
                .back-link {{ color: #007bff; text-decoration: none; }}
                .back-link:hover {{ text-decoration: underline; }}
                .actions {{ margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/customers" class="back-link">← Back to Customers</a>
                <h1>Customer Details</h1>
                
                <div class="detail-row">
                    <div class="detail-label">ID:</div>
                    <div class="detail-value">{customer.customer_id}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Name:</div>
                    <div class="detail-value">{customer.full_name}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Company:</div>
                    <div class="detail-value">{customer.company_name}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Title:</div>
                    <div class="detail-value">{customer.title}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Email:</div>
                    <div class="detail-value"><a href="mailto:{customer.email}">{customer.email}</a></div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">LinkedIn:</div>
                    <div class="detail-value">
                        {f'<a href="{customer.linkedin_url}" target="_blank">{customer.linkedin_url}</a>' if customer.linkedin_url else 'Not provided'}
                    </div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Status:</div>
                    <div class="detail-value">{'Active' if customer.is_active else 'Inactive'}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Created:</div>
                    <div class="detail-value">{customer.created_date.strftime('%Y-%m-%d %H:%M') if customer.created_date else 'Unknown'}</div>
                </div>
                
                <div class="actions">
                    {f'<a href="/email/generate/{customer.customer_id}" class="btn">Generate Email</a>' if is_admin else ''}
                    {f'<a href="/customers/edit/{customer.customer_id}" class="btn btn-secondary">Edit</a>' if is_admin else ''}
                    {f'<a href="/customers/delete/{customer.customer_id}" class="btn btn-danger" onclick="return confirm(\'Are you sure?\')">Delete</a>' if is_admin else ''}
                </div>
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
                <p><a href="/customers" class="back-link">← Back to Customers</a></p>
            </div>
        </body>
        </html>
        """
