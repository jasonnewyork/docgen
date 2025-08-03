"""
Email controller for AI email generation and management.
"""

import cherrypy
import logging
from business.services.email_service import EmailService
from business.services.customer_service import CustomerService
from web.controllers.auth_controller import AuthController


class EmailController:
    """Controller for email generation and management."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.email_service = EmailService()
        self.customer_service = CustomerService()
        self.auth = AuthController()
    
    @cherrypy.expose
    def index(self):
        """Redirect to email generation page."""
        raise cherrypy.HTTPRedirect('/email/generate')
    
    @cherrypy.expose
    def generate(self, customer_id=None, customer_ids=None, template_text=None, **kwargs):
        """Generate AI-powered email for one or more customers."""
        self.auth.require_admin()
        
        if cherrypy.request.method == 'GET':
            if customer_id:
                # Single customer selection
                try:
                    customer_id = int(customer_id)
                    customer = self.customer_service.get_customer_by_id(customer_id)
                    if not customer:
                        return self._render_error_page("Customer Not Found", f"Customer with ID {customer_id} not found")
                    return self._render_email_form([customer])
                except ValueError:
                    return self._render_error_page("Invalid Request", "Invalid customer ID")
            elif customer_ids:
                # Multiple customer selection
                try:
                    if isinstance(customer_ids, str):
                        customer_ids = [int(x.strip()) for x in customer_ids.split(',') if x.strip()]
                    elif isinstance(customer_ids, list):
                        customer_ids = [int(x) for x in customer_ids]
                    else:
                        customer_ids = [int(customer_ids)]
                    
                    customers = []
                    for cid in customer_ids:
                        customer = self.customer_service.get_customer_by_id(cid)
                        if customer:
                            customers.append(customer)
                    
                    if not customers:
                        return self._render_error_page("Customers Not Found", "No valid customers found")
                    
                    return self._render_email_form(customers)
                except ValueError:
                    return self._render_error_page("Invalid Request", "Invalid customer IDs")
            else:
                # Show customer selection
                customers = self.customer_service.get_active_customers()
                return self._render_customer_selection(customers)
        
        elif cherrypy.request.method == 'POST':
            try:
                # Get parameters from direct args or kwargs
                customer_ids = customer_ids or kwargs.get('customer_ids')
                template_text = template_text or kwargs.get('template_text', '')
                user_id = cherrypy.session.get('user_id')
                
                if not customer_ids:
                    customer_id = customer_id or kwargs.get('customer_id')
                    if customer_id:
                        customer_ids = [customer_id]
                
                if not customer_ids:
                    raise ValueError("Please select at least one customer")
                
                if not template_text.strip():
                    raise ValueError("Please provide template text")
                
                # Parse customer IDs
                if isinstance(customer_ids, str):
                    customer_ids = [int(x.strip()) for x in customer_ids.split(',') if x.strip()]
                elif not isinstance(customer_ids, list):
                    customer_ids = [int(customer_ids)]
                else:
                    customer_ids = [int(x) for x in customer_ids]
                
                # Get customers
                customers = []
                for cid in customer_ids:
                    customer = self.customer_service.get_customer_by_id(cid)
                    if customer:
                        customers.append(customer)
                
                if not customers:
                    raise ValueError("No valid customers selected")
                
                self.logger.info(f"Email generation - customers: {len(customers)}, template_text length: {len(template_text) if template_text else 0}")
                
                if len(customers) == 1:
                    # Single customer - existing behavior
                    email_log = self.email_service.generate_personalized_email(
                        customers[0], template_text, user_id
                    )
                    
                    raise cherrypy.HTTPRedirect(f'/email/preview/{email_log.email_log_id}')
                else:
                    # Multiple customers - bulk generation
                    email_logs = self.email_service.generate_bulk_personalized_emails(
                        customers, template_text, user_id
                    )
                    
                    # Redirect to bulk preview page
                    log_ids = ','.join(str(log.email_log_id) for log in email_logs)
                    raise cherrypy.HTTPRedirect(f'/email/bulk_preview?log_ids={log_ids}')
                
            except cherrypy.HTTPRedirect:
                # Re-raise HTTPRedirect - this is not an error, it's the normal flow
                raise
            except Exception as e:
                self.logger.error(f"Error generating email: {e}")
                if customer_ids:
                    try:
                        if isinstance(customer_ids, str):
                            customer_ids = [int(x.strip()) for x in customer_ids.split(',') if x.strip()]
                        customers = [self.customer_service.get_customer_by_id(cid) for cid in customer_ids if self.customer_service.get_customer_by_id(cid)]
                        return self._render_email_form(customers, kwargs, str(e))
                    except:
                        pass
                
                customers = self.customer_service.get_active_customers()
                return self._render_customer_selection(customers, str(e))
    
    @cherrypy.expose
    def preview(self, email_log_id):
        """Preview generated email before sending."""
        self.auth.require_admin()
        
        try:
            email_log_id = int(email_log_id)
            email_log = self.email_service.email_log_repository.get_by_id(email_log_id)
            
            if not email_log:
                return self._render_error_page("Email Not Found", f"Email log with ID {email_log_id} not found")
            
            customer = self.customer_service.get_customer_by_id(email_log.customer_id)
            return self._render_email_preview(email_log, customer)
            
        except ValueError:
            return self._render_error_page("Invalid Request", "Invalid email log ID")
        except Exception as e:
            self.logger.error(f"Error previewing email: {e}")
            return self._render_error_page("Error", str(e))
    
    @cherrypy.expose
    def send(self, email_log_id):
        """Send the generated email."""
        self.auth.require_admin()
        
        try:
            email_log_id = int(email_log_id)
            success = self.email_service.send_email(email_log_id)
            
            if success:
                raise cherrypy.HTTPRedirect('/email/logs?message=Email sent successfully')
            else:
                raise cherrypy.HTTPRedirect(f'/email/preview/{email_log_id}?error=Failed to send email')
                
        except ValueError:
            return self._render_error_page("Invalid Request", "Invalid email log ID")
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            raise cherrypy.HTTPRedirect(f'/email/preview/{email_log_id}?error=Failed to send email: {str(e)}')
    
    @cherrypy.expose
    def logs(self, message=None, error=None):
        """View email logs."""
        self.auth.require_auth()
        
        try:
            user_id = cherrypy.session.get('user_id')
            is_admin = cherrypy.session.get('is_admin', False)
            
            if is_admin:
                # Admins can see all emails
                email_logs = self.email_service.email_log_repository.get_all()
            else:
                # Regular users can only see their own emails
                email_logs = self.email_service.get_email_logs_by_user(user_id)
            
            return self._render_email_logs(email_logs, message, error)
            
        except Exception as e:
            self.logger.error(f"Error loading email logs: {e}")
            return self._render_error_page("Error", str(e))

    @cherrypy.expose
    def bulk_preview(self, log_ids=None):
        """Preview multiple generated emails before sending."""
        self.auth.require_admin()
        
        try:
            if not log_ids:
                return self._render_error_page("Missing Information", "No email logs specified")
            
            # Parse log IDs
            if isinstance(log_ids, str):
                log_ids = [int(x.strip()) for x in log_ids.split(',') if x.strip()]
            elif not isinstance(log_ids, list):
                log_ids = [int(log_ids)]
            else:
                log_ids = [int(x) for x in log_ids]
            
            # Get email logs and customers
            email_previews = []
            for log_id in log_ids:
                email_log = self.email_service.email_log_repository.get_by_id(log_id)
                if email_log:
                    customer = self.customer_service.get_customer_by_id(email_log.customer_id)
                    if customer:
                        email_previews.append({
                            'log': email_log,
                            'customer': customer
                        })
            
            if not email_previews:
                return self._render_error_page("No Valid Emails", "No valid email logs found")
            
            return self._render_bulk_email_preview(email_previews)
            
        except ValueError:
            return self._render_error_page("Invalid Request", "Invalid email log IDs")
        except Exception as e:
            self.logger.error(f"Error previewing bulk emails: {e}")
            return self._render_error_page("Error", str(e))

    @cherrypy.expose
    def bulk_send(self, log_ids=None):
        """Send multiple emails at once."""
        self.auth.require_admin()
        
        try:
            if not log_ids:
                return self._render_error_page("Missing Information", "No email logs specified")
            
            # Parse log IDs
            if isinstance(log_ids, str):
                log_ids = [int(x.strip()) for x in log_ids.split(',') if x.strip()]
            elif not isinstance(log_ids, list):
                log_ids = [int(log_ids)]
            else:
                log_ids = [int(x) for x in log_ids]
            
            # Send emails
            results = self.email_service.send_bulk_emails(log_ids)
            
            # Count successes and failures
            success_count = sum(1 for success in results.values() if success)
            total_count = len(results)
            
            if success_count == total_count:
                message = f"All {total_count} emails sent successfully!"
            else:
                message = f"{success_count} of {total_count} emails sent successfully. Check logs for failures."
            
            raise cherrypy.HTTPRedirect(f'/email/logs?message={message}')
            
        except ValueError:
            return self._render_error_page("Invalid Request", "Invalid email log IDs")
        except Exception as e:
            self.logger.error(f"Error sending bulk emails: {e}")
            return self._render_error_page("Error", str(e))
    
    def _render_customer_selection(self, customers, error=None):
        """Render customer selection page for email generation."""
        customer_options = ""
        for customer in customers:
            customer_options += f'<option value="{customer.customer_id}">{customer.full_name} ({customer.company_name})</option>'
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MyCRM - Select Customers for Email</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .form-group {{ margin-bottom: 20px; }}
                label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
                select {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }}
                .btn {{ padding: 12px 24px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; margin-right: 10px; }}
                .btn:hover {{ background-color: #0056b3; }}
                .btn-secondary {{ background-color: #6c757d; }}
                .btn-secondary:hover {{ background-color: #545b62; }}
                .error {{ color: red; margin-bottom: 15px; padding: 10px; background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 4px; }}
                .back-link {{ color: #007bff; text-decoration: none; }}
                .back-link:hover {{ text-decoration: underline; }}
                .selection-info {{ background-color: #e7f3ff; padding: 15px; border-radius: 4px; margin-bottom: 20px; }}
                .customer-count {{ font-weight: bold; color: #007bff; }}
                #customerSelect {{ height: 200px; }}
            </style>
            <script>
                function updateSelection() {{
                    const select = document.getElementById('customerSelect');
                    const count = select.selectedOptions.length;
                    const countSpan = document.getElementById('selectedCount');
                    const continueBtn = document.getElementById('continueBtn');
                    
                    countSpan.textContent = count;
                    continueBtn.disabled = count === 0;
                    
                    if (count === 0) {{
                        continueBtn.style.opacity = '0.5';
                    }} else {{
                        continueBtn.style.opacity = '1';
                    }}
                }}
                
                function selectAll() {{
                    const select = document.getElementById('customerSelect');
                    for (let option of select.options) {{
                        option.selected = true;
                    }}
                    updateSelection();
                }}
                
                function selectNone() {{
                    const select = document.getElementById('customerSelect');
                    for (let option of select.options) {{
                        option.selected = false;
                    }}
                    updateSelection();
                }}
                
                function continueToEmail() {{
                    const select = document.getElementById('customerSelect');
                    const selectedIds = Array.from(select.selectedOptions).map(option => option.value);
                    
                    if (selectedIds.length === 0) {{
                        alert('Please select at least one customer.');
                        return;
                    }}
                    
                    window.location.href = '/email/generate?customer_ids=' + selectedIds.join(',');
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <a href="/" class="back-link">← Back to Dashboard</a>
                <h1>Select Customers for Email Generation</h1>
                
                {f'<div class="error">{error}</div>' if error else ''}
                
                <div class="selection-info">
                    <strong>Instructions:</strong> Hold Ctrl (Windows) or Cmd (Mac) to select multiple customers. 
                    You can select one or more customers to generate personalized emails.
                    <br><br>
                    <span class="customer-count">Selected: <span id="selectedCount">0</span> customers</span>
                </div>
                
                <div class="form-group">
                    <label for="customerSelect">Select Customers:</label>
                    <select id="customerSelect" multiple onchange="updateSelection()">
                        {customer_options}
                    </select>
                </div>
                
                <div class="form-group">
                    <button type="button" class="btn btn-secondary" onclick="selectAll()">Select All</button>
                    <button type="button" class="btn btn-secondary" onclick="selectNone()">Clear Selection</button>
                </div>
                
                <button id="continueBtn" type="button" class="btn" onclick="continueToEmail()" disabled style="opacity: 0.5;">
                    Continue to Email Generation
                </button>
            </div>
        </body>
        </html>
        """
    
    def _render_email_form(self, customers, data=None, error=None):
        """Render email generation form for single or multiple customers."""
        data = data or {}
        
        # Handle both single customer (backward compatibility) and multiple customers
        if not isinstance(customers, list):
            customers = [customers]
        
        # Build customer info display
        customer_info_html = ""
        customer_ids = []
        
        if len(customers) == 1:
            customer = customers[0]
            customer_ids = [str(customer.customer_id)]
            customer_info_html = f"""
                <div class="customer-info">
                    <h3>Selected Customer</h3>
                    <p><strong>Name:</strong> {customer.full_name}</p>
                    <p><strong>Company:</strong> {customer.company_name}</p>
                    <p><strong>Title:</strong> {customer.title}</p>
                    <p><strong>Email:</strong> {customer.email}</p>
                </div>
            """
        else:
            customer_ids = [str(c.customer_id) for c in customers]
            customer_list = ""
            for customer in customers:
                customer_list += f"""
                    <div style="margin-bottom: 10px; padding: 10px; background-color: #f8f9fa; border-radius: 4px;">
                        <strong>{customer.full_name}</strong> ({customer.company_name})<br>
                        <small>{customer.title} - {customer.email}</small>
                    </div>
                """
            
            customer_info_html = f"""
                <div class="customer-info">
                    <h3>Selected Customers ({len(customers)} total)</h3>
                    {customer_list}
                </div>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MyCRM - Generate Email</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .customer-info {{ background-color: #f8f9fa; padding: 20px; border-radius: 6px; margin-bottom: 20px; max-height: 300px; overflow-y: auto; }}
                .form-group {{ margin-bottom: 20px; }}
                label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
                textarea {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; resize: vertical; }}
                .btn {{ padding: 12px 24px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; margin-right: 10px; }}
                .btn:hover {{ background-color: #0056b3; }}
                .btn-secondary {{ background-color: #6c757d; }}
                .btn-secondary:hover {{ background-color: #545b62; }}
                .error {{ color: red; margin-bottom: 15px; padding: 10px; background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 4px; }}
                .char-count {{ font-size: 12px; color: #666; margin-top: 5px; }}
                .back-link {{ color: #007bff; text-decoration: none; }}
                .back-link:hover {{ text-decoration: underline; }}
                .info {{ background-color: #d1ecf1; padding: 15px; border-radius: 4px; margin-bottom: 20px; }}
                .bulk-info {{ background-color: #fff3cd; padding: 15px; border-radius: 4px; margin-bottom: 20px; border: 1px solid #ffeaa7; }}
            </style>
            <script>
                function updateCharCount() {{
                    const textarea = document.getElementById('template_text');
                    const counter = document.getElementById('char-count');
                    const length = textarea.value.length;
                    counter.textContent = length + ' / 1000 characters';
                    
                    if (length > 900) {{
                        counter.style.color = 'red';
                    }} else if (length > 800) {{
                        counter.style.color = 'orange';
                    }} else {{
                        counter.style.color = '#666';
                    }}
                }}
                
                window.onload = function() {{
                    updateCharCount();
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <a href="/email/generate" class="back-link">← Select Different Customers</a>
                <h1>Generate Personalized Email{'s' if len(customers) > 1 else ''}</h1>
                
                {customer_info_html}
                
                {f'<div class="bulk-info"><strong>Bulk Email Generation:</strong> This template will be personalized for each customer using AI. Each customer will receive a uniquely generated email.</div>' if len(customers) > 1 else ''}
                
                <div class="info">
                    <strong>Template Variables:</strong> You can use placeholders like {{customer_name}}, {{company_name}}, etc. 
                    AI will automatically personalize the content for each customer.
                </div>
                
                {f'<div class="error">{error}</div>' if error else ''}
                
                <form method="post" action="/email/generate">
                    <input type="hidden" name="customer_ids" value="{','.join(customer_ids)}">
                    
                    <div class="form-group">
                        <label for="template_text">Email Template (max 1000 characters):</label>
                        <textarea id="template_text" name="template_text" rows="10" maxlength="1000" required
                                  oninput="updateCharCount()">{data.get('template_text', '')}</textarea>
                        <div class="char-count" id="char-count">0 / 1000 characters</div>
                    </div>
                    
                    <button type="submit" class="btn">Generate Email{'s' if len(customers) > 1 else ''}</button>
                    <a href="/email/generate" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </body>
        </html>
        """

    def _render_bulk_email_preview(self, email_previews):
        """Render bulk email preview page."""
        preview_items = ""
        log_ids = []
        
        for i, preview in enumerate(email_previews):
            email_log = preview['log']
            customer = preview['customer']
            log_ids.append(str(email_log.email_log_id))
            
            compliance_status = "✅ Approved" if email_log.compliance_approved else "❌ Rejected"
            compliance_color = "#28a745" if email_log.compliance_approved else "#dc3545"
            
            preview_items += f"""
                <div class="email-preview-item">
                    <div class="customer-header">
                        <h3>Email {i+1}: {customer.full_name} ({customer.company_name})</h3>
                        <span class="recipient">To: {customer.email}</span>
                    </div>
                    
                    <div class="email-content">
                        <div class="form-group">
                            <label>Subject:</label>
                            <div class="subject-line">{email_log.subject or 'No subject generated'}</div>
                        </div>
                        
                        <div class="form-group">
                            <label>Email Content:</label>
                            <div class="email-body">{email_log.generated_email or 'No content generated'}</div>
                        </div>
                    </div>
                    
                    <div class="compliance-info">
                        <h4>Compliance Check</h4>
                        <div class="compliance-details">
                            <strong>HIPAA Check:</strong><br>
                            {email_log.hipaa_compliance_check or 'Not checked'}
                        </div>
                        <div class="compliance-details">
                            <strong>Responsible AI Check:</strong><br>
                            {email_log.ai_compliance_check or 'Not checked'}
                        </div>
                        <p><strong>Overall Status:</strong> <span style="color: {compliance_color};">{compliance_status}</span></p>
                    </div>
                </div>
            """
        
        all_approved = all(preview['log'].compliance_approved for preview in email_previews)
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MyCRM - Bulk Email Preview</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .email-preview-item {{ margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9; }}
                .customer-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #ddd; }}
                .customer-header h3 {{ margin: 0; color: #333; }}
                .recipient {{ color: #666; font-style: italic; }}
                .email-content {{ margin-bottom: 20px; }}
                .form-group {{ margin-bottom: 15px; }}
                .form-group label {{ display: block; margin-bottom: 5px; font-weight: bold; color: #333; }}
                .subject-line {{ padding: 10px; background-color: white; border: 1px solid #ddd; border-radius: 4px; }}
                .email-body {{ padding: 15px; background-color: white; border: 1px solid #ddd; border-radius: 4px; line-height: 1.6; white-space: pre-wrap; }}
                .compliance-info {{ background-color: #f8f9fa; padding: 15px; border-radius: 6px; }}
                .compliance-details {{ margin-bottom: 10px; padding: 8px; background-color: white; border-radius: 4px; font-size: 14px; }}
                .btn {{ padding: 12px 24px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; margin-right: 10px; }}
                .btn:hover {{ background-color: #0056b3; }}
                .btn-success {{ background-color: #28a745; }}
                .btn-success:hover {{ background-color: #218838; }}
                .btn-secondary {{ background-color: #6c757d; }}
                .btn-secondary:hover {{ background-color: #545b62; }}
                .btn:disabled {{ background-color: #6c757d; opacity: 0.5; cursor: not-allowed; }}
                .back-link {{ color: #007bff; text-decoration: none; }}
                .back-link:hover {{ text-decoration: underline; }}
                .summary {{ background-color: #e7f3ff; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
                .summary h2 {{ margin-top: 0; color: #007bff; }}
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/email/generate" class="back-link">← Back to Email Generation</a>
                
                <div class="summary">
                    <h2>Bulk Email Preview</h2>
                    <p><strong>Total Emails:</strong> {len(email_previews)}</p>
                    <p><strong>Compliance Status:</strong> {len([p for p in email_previews if p['log'].compliance_approved])} approved, {len([p for p in email_previews if not p['log'].compliance_approved])} rejected</p>
                </div>
                
                {preview_items}
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
                    {f'<a href="/email/bulk_send?log_ids={",".join(log_ids)}" class="btn btn-success" onclick="return confirm(\'Send all {len(email_previews)} emails?\')">Send All Emails</a>' if all_approved else '<button class="btn" disabled>Send All Emails (Some Failed Compliance)</button>'}
                    <a href="/email/generate" class="btn btn-secondary">Edit Template</a>
                    <a href="/email/logs" class="btn">View Email History</a>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _render_email_preview(self, email_log, customer):
        """Render email preview page."""
        compliance_status = "✅ Approved" if email_log.compliance_approved else "❌ Rejected"
        compliance_color = "#28a745" if email_log.compliance_approved else "#dc3545"
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MyCRM - Email Preview</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .email-preview {{ background-color: #f8f9fa; padding: 20px; border-radius: 6px; margin: 20px 0; border: 1px solid #dee2e6; }}
                .compliance-section {{ margin: 20px 0; }}
                .compliance-item {{ background-color: #f8f9fa; padding: 15px; border-radius: 4px; margin-bottom: 10px; }}
                .btn {{ padding: 12px 24px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; margin-right: 10px; }}
                .btn:hover {{ background-color: #0056b3; }}
                .btn-success {{ background-color: #28a745; }}
                .btn-success:hover {{ background-color: #218838; }}
                .btn-secondary {{ background-color: #6c757d; }}
                .btn-secondary:hover {{ background-color: #545b62; }}
                .btn:disabled {{ background-color: #6c757d; cursor: not-allowed; }}
                .back-link {{ color: #007bff; text-decoration: none; }}
                .back-link:hover {{ text-decoration: underline; }}
                .status {{ font-weight: bold; color: {compliance_color}; }}
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/email/generate" class="back-link">← Generate New Email</a>
                <h1>Email Preview</h1>
                
                <h3>Recipient: {customer.full_name} ({customer.email})</h3>
                
                <div class="email-preview">
                    <p><strong>Subject:</strong> {email_log.subject}</p>
                    <hr>
                    <div style="white-space: pre-line;">{email_log.generated_email}</div>
                </div>
                
                <div class="compliance-section">
                    <h3>Compliance Review</h3>
                    
                    <div class="compliance-item">
                        <strong>HIPAA Compliance:</strong><br>
                        {email_log.hipaa_compliance_check}
                    </div>
                    
                    <div class="compliance-item">
                        <strong>AI Ethics Review:</strong><br>
                        {email_log.ai_compliance_check}
                    </div>
                    
                    <p><strong>Overall Status:</strong> <span class="status">{compliance_status}</span></p>
                </div>
                
                <div>
                    {f'<a href="/email/send/{email_log.email_log_id}" class="btn btn-success" onclick="return confirm(\'Send this email to {customer.email}?\')">Send Email</a>' if email_log.compliance_approved else '<button class="btn" disabled>Send Email (Compliance Failed)</button>'}
                    <a href="/email/generate/{customer.customer_id}" class="btn btn-secondary">Edit Template</a>
                    <a href="/email/logs" class="btn">View Email History</a>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _render_email_logs(self, email_logs, message=None, error=None):
        """Render email logs page."""
        log_rows = ""
        for log in email_logs:
            status = "✅ Sent" if log.email_sent else ("⏳ Pending" if log.compliance_approved else "❌ Rejected")
            log_rows += f"""
            <tr>
                <td>{log.email_log_id}</td>
                <td>{log.recipient_email}</td>
                <td>{log.subject[:50]}{'...' if len(log.subject) > 50 else ''}</td>
                <td>{status}</td>
                <td>{log.sent_date.strftime('%Y-%m-%d %H:%M') if log.sent_date else 'Not sent'}</td>
                <td>
                    <a href="/email/preview/{log.email_log_id}" class="btn btn-sm">View</a>
                </td>
            </tr>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MyCRM - Email History</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f8f9fa; font-weight: bold; }}
                .btn {{ display: inline-block; padding: 6px 12px; text-decoration: none; background-color: #007bff; color: white; border-radius: 4px; }}
                .btn:hover {{ background-color: #0056b3; }}
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
                        <h1>Email History</h1>
                    </div>
                    <a href="/email/generate" class="btn">Generate New Email</a>
                </div>
                
                {f'<div class="message">{message}</div>' if message else ''}
                {f'<div class="error">{error}</div>' if error else ''}
                
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Recipient</th>
                            <th>Subject</th>
                            <th>Status</th>
                            <th>Sent Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {log_rows if log_rows else '<tr><td colspan="6">No email logs found</td></tr>'}
                    </tbody>
                </table>
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
                <p><a href="/email/generate" class="back-link">← Back to Email Generation</a></p>
            </div>
        </body>
        </html>
        """
