-- MyCRM Database Schema
-- SQL Server database setup script

-- Create database (if needed)
-- CREATE DATABASE MyCRM;
-- USE MyCRM;

-- Create roles table
CREATE TABLE roles (
    role_id INT IDENTITY(1,1) PRIMARY KEY,
    role_name NVARCHAR(50) NOT NULL UNIQUE,
    description NVARCHAR(255),
    created_date DATETIME2 DEFAULT GETDATE()
);
GO

-- Create users table
CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    email NVARCHAR(255) NOT NULL UNIQUE,
    first_name NVARCHAR(100) NOT NULL,
    last_name NVARCHAR(100) NOT NULL,
    password_hash NVARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    is_active BIT DEFAULT 1,
    created_date DATETIME2 DEFAULT GETDATE(),
    last_login_date DATETIME2 NULL,
    CONSTRAINT FK_Users_Roles FOREIGN KEY (role_id) REFERENCES roles(role_id)
);
GO

-- Create customers table
CREATE TABLE customers (
    customer_id INT IDENTITY(1,1) PRIMARY KEY,
    company_name NVARCHAR(255) NOT NULL,
    contact_first_name NVARCHAR(100),
    contact_last_name NVARCHAR(100),
    contact_email NVARCHAR(255),
    contact_phone NVARCHAR(50),
    address NVARCHAR(255),
    city NVARCHAR(100),
    state NVARCHAR(100),
    country NVARCHAR(100),
    postal_code NVARCHAR(20),
    industry NVARCHAR(100),
    created_date DATETIME2 DEFAULT GETDATE(),
    last_modified_date DATETIME2 DEFAULT GETDATE(),
    is_active BIT DEFAULT 1
);
GO

-- Create email_logs table
CREATE TABLE email_logs (
    log_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT,
    user_id INT NOT NULL,
    email_type NVARCHAR(50) NOT NULL,
    subject NVARCHAR(255) NOT NULL,
    content NTEXT NOT NULL,
    recipient_email NVARCHAR(255) NOT NULL,
    sent_date DATETIME2 DEFAULT GETDATE(),
    status NVARCHAR(50) DEFAULT 'Pending',
    error_message NTEXT NULL,
    CONSTRAINT FK_EmailLogs_Customers FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT FK_EmailLogs_Users FOREIGN KEY (user_id) REFERENCES users(user_id)
);
GO

-- Create indexes for better performance
CREATE INDEX IX_Users_Username ON users(username);
CREATE INDEX IX_Users_Email ON users(email);
CREATE INDEX IX_Customers_CompanyName ON customers(company_name);
CREATE INDEX IX_Customers_ContactEmail ON customers(contact_email);
CREATE INDEX IX_EmailLogs_CustomerID ON email_logs(customer_id);
CREATE INDEX IX_EmailLogs_UserID ON email_logs(user_id);
CREATE INDEX IX_EmailLogs_SentDate ON email_logs(sent_date);
GO

-- Insert default roles
INSERT INTO roles (role_name, description) VALUES 
    ('Administrator', 'Full system access and user management'),
    ('User', 'Standard user access to customer and email features'),
    ('Read-Only', 'View-only access to data');
GO

-- Insert default admin user (password: admin123)
-- Password hash for 'admin123' using bcrypt
INSERT INTO users (username, email, first_name, last_name, password_hash, role_id) VALUES 
    ('admin', 'admin@mycrm.com', 'System', 'Administrator', 
     '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeU8cIsP7EIlJA2Xe', 1);
GO

-- Insert sample customers for testing
INSERT INTO customers (company_name, contact_first_name, contact_last_name, contact_email, contact_phone, address, city, state, country, postal_code, industry) VALUES 
    ('Acme Corporation', 'John', 'Smith', 'john.smith@acme.com', '555-0101', '123 Business Ave', 'Seattle', 'WA', 'USA', '98101', 'Technology'),
    ('Global Dynamics', 'Sarah', 'Johnson', 'sarah.johnson@globaldynamics.com', '555-0102', '456 Industry Blvd', 'Portland', 'OR', 'USA', '97201', 'Manufacturing'),
    ('Tech Solutions Inc', 'Michael', 'Davis', 'michael.davis@techsolutions.com', '555-0103', '789 Innovation Dr', 'San Francisco', 'CA', 'USA', '94102', 'Technology'),
    ('Healthcare Partners', 'Emily', 'Wilson', 'emily.wilson@healthcarepartners.com', '555-0104', '321 Medical Center Way', 'Los Angeles', 'CA', 'USA', '90210', 'Healthcare'),
    ('Financial Services Group', 'Robert', 'Brown', 'robert.brown@financialgroup.com', '555-0105', '654 Wall Street', 'New York', 'NY', 'USA', '10001', 'Finance');
GO

PRINT 'Database schema created successfully!';
PRINT 'Default admin user: admin / admin123';
PRINT 'Sample customers have been added for testing.';
