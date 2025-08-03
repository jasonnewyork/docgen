
# Software Requirements Specification for .NET
## For MyCRM

Version 0.1  
Prepared by Jason Hogg  
7/27/2025

Table of Contents
=================
* [Revision History](#revision-history)
* 1 [Introduction](#1-introduction)
  * 1.1 [Document Purpose](#11-document-purpose)
  * 1.2 [Product Scope](#12-product-scope)
  * 1.3 [Definitions, Acronyms and Abbreviations](#13-definitions-acronyms-and-abbreviations)
  * 1.4 [References](#14-references)
  * 1.5 [Document Overview](#15-document-overview)
* 2 [Product Overview](#2-product-overview)
  * 2.1 [Product Perspective](#21-product-perspective)
  * 2.2 [Product Functions](#22-product-functions)
  * 2.3 [Product Constraints](#23-product-constraints)
  * 2.4 [User Characteristics](#24-user-characteristics)
  * 2.5 [Assumptions and Dependencies](#25-assumptions-and-dependencies)
  * 2.6 [Apportioning of Requirements](#26-apportioning-of-requirements)
* 3 [Requirements](#3-requirements)
  * 3.1 [External Interfaces](#31-external-interfaces)
    * 3.1.1 [User Interfaces](#311-user-interfaces)
    * 3.1.2 [Hardware Interfaces](#312-hardware-interfaces)
    * 3.1.3 [Software Interfaces](#313-software-interfaces)
    * 3.1.4 [Database Design](#314-database-design)
  * 3.2 [Functional](#32-functional)
  * 3.3 [Quality of Service](#33-quality-of-service)
    * 3.3.1 [Performance](#331-performance)
    * 3.3.2 [Security](#332-security)
    * 3.3.3 [Reliability](#333-reliability)
    * 3.3.4 [Availability](#334-availability)
  * 3.4 [Compliance](#34-compliance)
* 4 [Design and Implementation](#4-design-and-implementation)
  * 4.1 [Enterprise Application Reference Architecture](#41-enterprise-application-reference-architecture)
  * 4.2 [Enterprise Application Implementation Details](#42-enterprise-application-implementation-details)
  * 4.3 [Installation](#43-installation)
  * 4.4 [Distribution](#44-distribution)
  * 4.5 [Maintainability](#45-maintainability)
  * 4.6 [Reusability](#46-reusability)
  * 4.7 [Portability](#47-portability)
  * 4.8 [Cost](#48-cost)
  * 4.9 [Deadline](#49-deadline)
  * 4.10 [Proof of Concept](#410-proof-of-concept)
* 5 [Verification](#5-verification)
* 6 [Appendixes](#6-appendixes)

## Revision History
| Name | Date    | Reason For Changes  | Version   |
| ---- | ------- | ------------------- | --------- |
| Reqs | 7/27/25 | Initial draft       |    0.1    |
|      | 8/2/25  | Update for .NET     |    0.2    |
|      |         |                     |           |

## 1. Introduction
The goal of this document is to provide a detailed description of the requirements for our new customer relationship management system - henceforth referred to as MyCRM. 

> This section should provide an overview of the entire document

### 1.1 Document Purpose
This document provides functional and non-functional requirements for the new MyCRM system. 

### 1.2 Product Scope
<!-- Identify the product whose software requirements are specified in this document, including the revision or release number. Explain what the product that is covered by this SRS will do, particularly if this SRS describes only part of the system or a single subsystem. Provide a short description of the software being specified and its purpose, including relevant benefits, objectives, and goals. Relate the software to corporate goals or business strategies. If a separate vision and scope document is available, refer to it rather than duplicating its contents here. -->
MyCRM is a new web application that will enable its users to track its customers and use AI to generate content as the basis for initiating and following up with customers. This specification document provides initial requirements for the MVP solution with the expectation that  new scenarios and requirements will emerge over time. 

### 1.3 Definitions, Acronyms and Abbreviations
 - CRM: Customer Relationship Management
 - CRUD: Create, Read, Update, Delete operations
 - GenAI: Generative Artificial Intelligence
 - HIPAA: Health Insurance Portability and Accountability Act
 - RBAC: Role-Based Access Control
 - SMTP: Simple Mail Transfer Protocol
 - API: Application Programming Interface
 - SQL: Structured Query Language
 - UI: User Interface
 - MVC: Model-View-Controller architecture pattern
 - [AI] ASP.NET: Microsoft's web application framework for .NET
 - [AI] Entity Framework: Microsoft's Object-Relational Mapping (ORM) framework
 - Kestrel - the default web server for .net core applications 
 - [AI] JWT: JSON Web Token for secure authentication
 - [AI] CORS: Cross-Origin Resource Sharing

### 1.4 References
<!-- List any other documents or Web addresses to which this SRS refers. These may include user interface style guides, contracts, standards, system requirements specifications, use case documents, or a vision and scope document. Provide enough information so that the reader could access a copy of each reference, including title, author, version number, date, and source or location.--> 

### 1.5 Document Overview
 This document is organized into five main sections:
 - Section 1 provides an introduction and overview of the MyCRM system
 - Section 2 describes the product overview including functions, constraints, and user characteristics
 - Section 3 specifies detailed functional and non-functional requirements
 - Section 4 outlines the verification and testing approach
 - Section 5 contains appendixes with additional reference material

## 2. Product Overview
MyCRM is a new customer relationship management application that is being developed. 
<!-- >> This section should describe the general factors that affect the product and its requirements. This section does not state specific requirements. Instead, it provides a background for those requirements, which are defined in detail in Section 3, and makes them easier to understand. -->

### 2.1 Product Perspective
<!-- Describe the context and origin of the product being specified in this SRS. For example, state whether this product is a follow-on member of a product family, a replacement for certain existing systems, or a new, self-contained product. If the SRS defines a component of a larger system, relate the requirements of the larger system to the functionality of this software and identify interfaces between the two. A simple diagram that shows the major components of the overall system, subsystem interconnections, and external interfaces can be helpful. -->
The application should be designed to run initially as a standalone multi-ter web application that can also in the future be depoyed to Microsoft Azure's cloud with minimal changes. 

### 2.2 Product Functions
<!-- Summarize the major functions the product must perform or must let the user perform. Details will be provided in Section 3, so only a high level summary (such as a bullet list) is needed here. Organize the functions to make them understandable to any reader of the SRS. A picture of the major groups of related requirements and how they relate, such as a top level data flow diagram or object class diagram, is often effective. -->
There are two major business scenarios the application will focus on initially

1. Customer management - Functionality to manage the customers including the ability to:
1a. List customers - list all the customers in a table along with their details
1b. Add customer - functionality to add a new customer 
1c. Edit customer - the ability to edit a customer
1d. Delete customer - the ability to delete a customer. Deletions should be soft deletes - meaning the database retains the customer yet has a flag to track that the customer is deleted.

3. Customer outreach email - Functionality to enable an outreach email to be generated using GenAI. This functionality should allow:
-  One or more customer(s) to be selected from the list of active customers 
- Outreach template text to be provided. This should allow for 1000 characters of text to be provided that will provide the template for the email that will be sent. 
- Email preview - use  GenAI  to take the outreach template text and personalize including relevant user details such as contact name and / or company name from the selected user
- Email send - allow the user to then have the email be sent after approving the email preview 
- All emails sent must be stored in a database table for auditing purposes
-   Bulk email generation - when multiple customers are selected, the system shall generate personalized emails for each customer individually
-   Bulk email preview - display all generated emails in a summary view before sending
-   Bulk email sending - allow sending all approved emails with a single action

### 2.3 Product Constraints
<!--This subsection should provide a general description of any other items that will limit the developer’s options. These may include:  

* Interfaces to users, other applications or hardware.  
* Quality of service constraints.  
* Standards compliance.  
* Constraints around design or implementation. -->
After GenAI has been used to synthesize an email we need to review the generated text against Microsoft's responsible AI principles and summarize whether the email violates any of the principles. A summary must be provided before the email can be sent.  

### 2.4 User Characteristics
<!--Identify the various user classes that you anticipate will use this product. User classes may be differentiated based on frequency of use, subset of product functions used, technical expertise, security or privilege levels, educational level, or experience. Describe the pertinent characteristics of each user class. Certain requirements may pertain only to certain user classes. Distinguish the most important user classes for this product from those who are less important to satisfy. -->
For the first version of this product there will be two user roles.
1. Power user - The power user can use both the customer management and customer outreach mail functionality.
2. Customer manager - This user can only use the customer management functionality and cannot use the customer outreach mail functionality.

### 2.5 Assumptions and Dependencies
<!-- List any assumed factors (as opposed to known facts) that could affect the requirements stated in the SRS. These could include third-party or commercial components that you plan to use, issues around the development or operating environment, or constraints. The project could be affected if these assumptions are incorrect, are not shared, or change. Also identify any dependencies the project has on external factors, such as software components that you intend to reuse from another project, unless they are already documented elsewhere (for example, in the vision and scope document or the project plan).--> 

This is a brand new system. It will initially be hosted on Windows Server and will be deployed on a locally managed servers but over time will likely move to Microsoft Azure. 

### 2.6 Apportioning of Requirements
<!-- Apportion the software requirements to software elements. For requirements that will require implementation over multiple software elements, or when allocation to a software element is initially undefined, this should be so stated. A cross reference table by function and software element should be used to summarize the apportioning.

Identify requirements that may be delayed until future versions of the system (e.g., blocks and/or increments). -->

The application should be constructed as multi-tier web application
1. Modern web browser like Edge, Firefox, Chrome etc
2. Service layer - Web server hosting services that encapsulate business logic 
3. Database - Microsoft SQL server 


## 3. Requirements
<!-- 
> This section specifies the software product's requirements. Specify all of the software requirements to a level of detail sufficient to enable designers to design a software system to satisfy those requirements, and to enable testers to test that the software system satisfies those requirements.

> The specific requirements should:
* Be uniquely identifiable.
* State the subject of the requirement (e.g., system, software, etc.) and what shall be done.
* Optionally state the conditions and constraints, if any.
* Describe every input (stimulus) into the software system, every output (response) from the software system, and all functions performed by the software system in response to an input or in support of an output.
* Be verifiable (e.g., the requirement realization can be proven to the customer's satisfaction)
* Conform to agreed upon syntax, keywords, and terms.
--> 

The system shall support at minimum the following functional requirements:
- REQ-100 - The system shall allow administrators to list, add, edit and delete customers
- REQ-101 - The customer management logic will verify all fields for format correctness and mandatory vs optional fields
- REQ-102 -  The system shall provide customer search functionality by name, company, and email
- REQ-103 -  The system shall implement soft delete functionality for customers (logical deletion)
- REQ-200 - The system shall allow administrators to list, create new users - either adminstrators or standard users
- REQ-201 - The user management logic will verify all fields for format correctness and mandatory vs optional fields
- REQ-202 -  The system shall provide secure password hashing using bcrypt algorithm
- REQ-203 -  The system shall support role-based access control with Administrator and User roles
- REQ-300 - The system shall allow users to create an email template for a specific customer and then use GenAI to personalize the email
- REQ-301 -  The system shall validate generated emails for HIPAA compliance before sending
- REQ-302 -  The system shall validate generated emails against Microsoft Responsible AI principles
- REQ-303 -  The system shall provide email preview functionality before sending
- REQ-304 -  The system shall log all email activities for audit purposes
- REQ-305 -  The system shall support multiple email types (introduction, follow-up, promotional, meeting request)
- REQ-306 -   The system shall support bulk email generation for multiple customers from a single template
- REQ-307 -   The system shall provide bulk email preview functionality showing all generated emails before sending
- REQ-308 -   The system shall support bulk email sending with individual compliance validation for each email
- [AI] REQ-400 - The system shall implement proper exception handling with user-friendly error messages
- [AI] REQ-401 - The system shall support configuration management through appsettings.json and environment variables
- [AI] REQ-402 - The system shall implement input validation and sanitization for all user inputs
- [AI] REQ-403 - The system shall support database connection pooling and transaction management
- [AI] REQ-404 - The system shall implement proper session management with configurable timeout
- [AI] REQ-405 - The system shall support API versioning for future extensibility
- [AI] REQ-406 - The system shall implement comprehensive logging using structured logging patterns
- [AI] REQ-407 - The system shall support health checks for monitoring system status


### 3.1 External Interfaces
<!-- >
> This subsection defines all the inputs into and outputs requirements of the software system. Each interface defined may include the following content:
* Name of item
* Source of input or destination of output
* Valid range, accuracy, and/or tolerance
* Units of measure
* Timing
* Relationships to other inputs/outputs
* Screen formats/organization
* Window formats/organization
* Data formats
* Command formats
* End messages --> 

#### 3.1.1 User interfaces
<!-- Define the software components for which a user interface is needed. Describe the logical characteristics of each interface between the software product and the users. This may include sample screen images, any GUI standards or product family style guides that are to be followed, screen layout constraints, standard buttons and functions (e.g., help) that will appear on every screen, keyboard shortcuts, error message display standards, and so on. Details of the user interface design should be documented in a separate user interface specification.

Could be further divided into Usability and Convenience requirements. --> 

The web application should include web pages for:
 - User authentication and login/logout functionality
 - Dashboard with system overview and navigation
- Customer CRUD operations
- Employee CRUD operations
- Email create / preview operations
- Administrative functions including a screen to change between mock repository and SQL repository
 - Email audit log viewing for administrators
 - Responsive design supporting desktop and mobile browsers

#### 3.1.2 Hardware interfaces
<!-- Describe the logical and physical characteristics of each interface between the software product and the hardware components of the system. This may include the supported device types, the nature of the data and control interactions between the software and the hardware, and communication protocols to be used. -->

The system will be deployed on Windows initially, but may also run on Linux Ubuntu with minimal changes.

#### 3.1.3 Software interfaces
<!-- Describe the connections between this product and other specific software components (name and version), including databases, operating systems, tools, libraries, and integrated commercial components. Identify the data items or messages coming into the system and going out and describe the purpose of each. Describe the services needed and the nature of communications. Refer to documents that describe detailed application programming interface protocols. Identify data that will be shared across software components. If the data sharing mechanism must be implemented in a specific way (for example, use of a global data area in a multitasking operating system), specify this as an implementation constraint. --> 

Email sending dependency:
- The system should use a library similar to CDOSYS or .NETs System.Net.Mail for sending emails
 - The system shall use .NET's library for email sending functionality
 - The system shall support configurable SMTP server settings via environment variables
 - The system shall use OpenAI GPT-3.5-turbo model for email content generation
 - The system shall integrate with OpenAI API using the official .NET client library

#### 3.1.4 Database design 

The backend database should support at minimum the following entities: 
1. Customer = including at least the following attributes: 
- First Name - string, 50 characters
- Last Name - string, 50 characters
- Company Name - string, 100 characters
- Title - string, 50 characters
- Email - string, 50 characters
- LinkedIn reference URL - string, 255 characters
- Active flag (for logical deletions) - bool
 - Customer ID - auto-incrementing integer primary key
 - Created Date - datetime field with default current timestamp
 - Modified Date - datetime field updated on each record change

2. Customer outreach email log - table to store generated emails including:
- Template text - string, 2000 characters
- Email preview - string, 2000 characters
- GenAI analysis of email for HIPPA compliance - string, 2000 characters
- Email address sent to - string, 255 characters
- Email date sent - datetime 
 - Email Log ID - auto-incrementing integer primary key
 - Customer ID - foreign key reference to Customer table
 - User ID - foreign key reference to User table
 - Email Type - string, 50 characters (introduction, follow-up, promotional, meeting_request)
 - Subject - string, 255 characters
 - Status - string, 50 characters (pending, sent, failed)
 - Error Message - string, 2000 characters for failure details

3. User authentication table
- User name - string, 50 characters
- Password - string, 50 characters
- Role - FK for user role table
- Active flag (for logical deletions) - bool
 - User ID - auto-incrementing integer primary key
 - Email - string, 255 characters (unique)
 - First Name - string, 100 characters
 - Last Name - string, 100 characters
 - Password Hash - string, 255 characters (bcrypt hashed)
 - Created Date - datetime field with default current timestamp
 - Last Login Date - datetime field updated on successful login

4. User role table
- Role name - string, 50 characters
- Role description - string, 255 characters
 - Role ID - auto-incrementing integer primary key
 - Created Date - datetime field with default current timestamp

### 3.2 Functional
 The system shall implement the following specific functional requirements:

 **Customer Management Functions:**
 - REQ-F100: User can view paginated list of active customers with search capability
 - REQ-F101: User can add new customer with validation of required fields
 - REQ-F102: User can edit existing customer information
 - REQ-F103: User can perform soft delete of customers (logical deletion)
 - REQ-F104: System validates email format and LinkedIn URL format
 - REQ-F105: System prevents duplicate customer email addresses

 **User Management Functions:**
 - REQ-F200: Administrator can view list of all system users
 - REQ-F201: Administrator can create new user accounts with role assignment
 - REQ-F202: Administrator can edit user information and reset passwords
 - REQ-F203: Administrator can activate/deactivate user accounts
 - REQ-F204: System enforces unique usernames and email addresses

 **Authentication Functions:**
 - REQ-F300: User can log in with username/password credentials
 - REQ-F301: System maintains secure user sessions
 - REQ-F302: User can log out and invalidate session
 - REQ-F303: System enforces role-based access control

 **Email Generation Functions:**
 - REQ-F400: User can select customer for email generation
 - REQ-F401: User can choose email type (introduction, follow-up, promotional, meeting request)
 - REQ-F402: User can input template text up to 1000 characters
 - REQ-F403: System generates personalized email using AI with customer data
 - REQ-F404: System validates generated content for compliance
 - REQ-F405: User can preview and edit generated email before sending
 - REQ-F406: System sends email and logs all details for audit
  - REQ-F407: User can select multiple customers for bulk email generation
  - REQ-F408: System generates personalized emails for each selected customer individually
  - REQ-F409: User can preview all generated emails in bulk preview interface
  - REQ-F410: System supports bulk sending of approved emails with individual compliance validation 

 **[AI] System Administration Functions:**
 - [AI] REQ-F500: Administrator can view system health dashboard with key metrics
 - [AI] REQ-F501: Administrator can configure system settings through admin interface
 - [AI] REQ-F502: Administrator can view and manage error logs
 - [AI] REQ-F503: Administrator can export audit data for compliance reporting
 - [AI] REQ-F504: System supports backup and restore operations for critical data

 **[AI] API and Integration Functions:**
 - [AI] REQ-F600: System shall expose RESTful APIs for customer management operations
 - [AI] REQ-F601: System shall implement API authentication using JWT tokens
 - [AI] REQ-F602: System shall support API rate limiting and throttling
 - [AI] REQ-F603: System shall provide API documentation using Swagger/OpenAPI 

### 3.3 Quality of Service
<!-- >> This section states additional, quality-related property requirements that the functional effects of the software should present. --> 
All exceptions that occur should be written to an error log file including: datetime, error number, error description, component source of error and any other relevant information
 - The system shall implement comprehensive logging using .NET's logging module
 - Log files shall be stored in the logs/ directory with rotation policy
 - Error logs shall include stack trace information for debugging
 - The system shall log all user authentication attempts (success and failure)
 - The system shall log all database operations and email sending activities

#### 3.3.1 Performance
<!--
If there are performance requirements for the product under various circumstances, state them here and explain their rationale, to help the developers understand the intent and make suitable design choices. Specify the timing relationships for real time systems. Make such requirements as specific as possible. You may need to state performance requirements for individual functional requirements or features. -->
The system should deliver all web pages to end users in under one second. The system should include telemetry for tracking TTFB and TTLB for each page along with content for a site adminstrator to view historical page load times and track % of pages delivered in under one second etc.
 - The system shall implement request timing middleware to measure page response times
 - Performance metrics shall be logged for administrative monitoring
 - The system shall be optimized for minimal database query overhead using connection pooling
 - Static assets (CSS, JavaScript, images) shall be served efficiently with appropriate caching headers 

#### 3.3.2 Security
<!-- Specify any requirements regarding security or privacy issues surrounding use of the product or protection of the data used or created by the product. Define any user identity authentication requirements. Refer to any external policies or regulations containing security issues that affect the product. Define any security or privacy certifications that must be satisfied. --> 

Authentication requirements:
- The system will eventually be deployed on Azure and will use its Entra / oauth based authentication mechanism, however we also want to be able to run initially without Azure so the system should have a configurable authentication mechanism allowing for local authentication or Azure based authentication.
- For the local mechanism create a SQL table with users + ids + passwords to use as the basis for authentication. Make sure passwords are stored securely.

Authorization requirements:
- The system will eventually be deployed on Azure and will use Azure RBAC as the basis for authorization, however we also want to be able to run initially without Azure so the system should also have a basic authorization mechanism allowing for local authorization or Azure RBAC based authorization.
- For the initial authorization logic there should be two roles - administrator which can perform read + write operations, and a standard user which can only perform read only operations. 

User registration:
- The system should have a screen that only adminstrators can use that allow new users to be added / edited / deleted - and for passwords to be reset. 
- The adminstrator can determine whether a user is an admin or a standard user

Database security requirements: 
The system should be secure with at least the following factors considered:
- Database accounts - a new SQL account should be created for the service layer to authenticate with database against 
- Database authentication - no passwords should be stored in code at all. Passwords will be referenced in system environment variables.  

Additional security requirements: 
- Web server session state should be secured appropriately to ensure users have to be authenticated before accessing the web application
- Database queries - all queries from service layer should be evaluated for threats such as sql injection


#### 3.3.3 Reliability
<!-- Specify the factors required to establish the required reliability of the software system at time of delivery. --> 

#### 3.3.4 Availability
<!-- Specify the factors required to guarantee a defined availability level for the entire system such as checkpoint, recovery, and restart. --> 

### 3.4 Compliance
<!-- Specify the requirements derived from existing standards or regulations, including:  
* Report format
* Data naming
* Accounting procedures
* Audit tracing

For example, this could specify the requirement for software to trace processing activity. Such traces are needed for some applications to meet minimum regulatory or financial standards. An audit trace requirement may, for example, state that all changes to a payroll database shall be recorded in a trace file with before and after values. -->

Health Care Industry Compliance Requirements: 
- This system is initially being deployed for a health care customer so its important to ensure HIPPA requirements are being considered including - how customer data is being stored as well as any requirements related to the information that is generated in the mock emails. 
- The system should also keep a log of all emails that are sent. Prior to sending the proposed email should be sent to the GenAI service to determine suitability for sending according to HIPPA regulations.  
- In the future it is possible that other industries compliance requirements will also have to be met - so ensure the HIPPA logic is configurable. 

Responsible AI Requirements:
- Given the system is using AI to personalize the email also include a requirement to verify the generated email against Microsoft's responsible AI principles - in addition to any HIPPA requirements.

### 4.0 Design and Implementation

#### 4.1 Enterprise Application Reference Architecture

The application shall follow our standard enterprise application reference architecture including:

Multi-Layer Architecture:
- Presentation Layer: Web browser, HTML templates, CSS, JavaScript
- Web Application Layer: ASP.NET for MVC framework, controllers, routing
- Business Logic Layer: Service classes, validation, error handling
- Data Access Layer: Repository pattern with factory for switching between live SQL and mock data. Default to live, if SQL not available switch to mock. 
- Data Persistence: SQL Server database and mock implementations

Design Patterns Showcased:
- Repository Pattern with automatic fallback (Database → Mock)
- Factory Pattern for repository creation
- MVC Architecture with clear separation of concerns
- Active Record for domain object persistence
- Service Layer for business logic centralization
- Dependency Injection for loose coupling

Adaptive Architecture:
- The system automatically detects available resources and switches between:

Database Mode: Full SQL Server integration
- Mock Mode: In-memory data for development/testing
- Auto-Detection: Seamless fallback based on environment

#### 4.2 Enterprise Application Implementation Details

Summary of assumed platform dependencies:
- C# and .NET as the programming language
- .NET as the web framework allowing for local deployment and also Azure deployment 
- OpenAI GPT-3.5 as basis for GenAI. OpenAI auth key is stored in "OPENAI_API_KEY" system environment variable
-  Microsoft SQL server as the database for storing customers. Connection string should be configurable - but initially assume localhost, mixed model authentication with SA account and password stored in "SQL_PASSWORD" system environment variable
 - bcrypt library for secure password hashing
 - .NET library for SQL Server database connectivity
 - .NET environment variable management
 - nunit for unit testing and code coverage
 - Use .NET 9
 - [AI] ASP.NET for web application framework
 - [AI] Entity Framework Core for database operations and ORM
 - [AI] AutoMapper for object-to-object mapping
 - [AI] Serilog for structured logging
 - [AI] FluentValidation for model validation
 - [AI] Swashbuckle.AspNetCore for API documentation
 - [AI] Microsoft.AspNetCore.Authentication.JwtBearer for JWT authentication
 - [AI] Microsoft.Extensions.Configuration for configuration management

#### 4.3 Installation
<!-- Constraints to ensure that the software-to-be will run smoothly on the target implementation platform.-->

Database scripts should be created for creating a database called "CRMDb", sql accounts and tables with appropriate names based on business requirements.
 - The system shall include comprehensive database setup scripts (schema.sql)
 - Database scripts shall create all required tables with proper indexes for performance
 - Scripts shall include sample data for development and testing purposes
 - Default administrator user account shall be created with secure default password
 - Database scripts shall be idempotent and safe to run multiple times  

#### 4.4 Distribution
<!-- Constraints on software components to fit the geographically distributed structure of the host organization, the distribution of data to be processed, or the distribution of devices to be controlled. --> 

#### 4.5 Maintainability
<!-- Specify attributes of software that relate to the ease of maintenance of the software itself. These may include requirements for certain modularity, interfaces, or complexity limitation. Requirements should not be placed here just because they are thought to be good design practices. -->
Unit tests should be created to support all generated code.

Functional tests should also be created covering at least the following end-to-end use cases:
- Create customer
- List all active customers
- Delete customer
- Generate email for a customer
- Send email to a customer
 - Unit tests shall achieve minimum 80% code coverage
 - Tests shall include mock data repositories for isolated testing
 - Integration tests shall verify database connectivity and operations
 - Email generation tests shall include AI service mocking for reliable testing
 - Authentication and authorization tests shall verify security requirements
 - Performance tests shall validate page load time requirements 

#### 4.6 Reusability
<!-- TODO: come up with a description -->
[AI] The application shall be designed with reusability in mind:
- [AI] Business logic shall be separated into service classes that can be reused across different interfaces
- [AI] Data access layer shall use repository pattern to allow different data sources
- [AI] Configuration management shall support multiple environments (dev, test, prod)
- [AI] API endpoints shall be designed for potential future mobile application integration
- [AI] Email templates shall be configurable and reusable across different campaigns
- [AI] Authentication and authorization components shall be modular for future Azure AD integration

#### 4.7 Portability
<!-- Specify attributes of software that relate to the ease of porting the software to other host machines and/or operating systems. -->
The solution will initially be created and deployed on Windows OS on ARM architecture, but might in time require either Windows Intel architecture and or even Linux Ubuntu support.  

#### 4.8 Cost
<!-- Specify monetary cost of the software product. -->

#### 4.9 Deadline
<!-- Specify schedule for delivery of the software product. --> 

#### 4.10 Proof of Concept
<!-- TODO: come up with a description -->
[AI] The proof of concept shall demonstrate:
- [AI] Successful integration with OpenAI API for email generation
- [AI] Database connectivity and basic CRUD operations
- [AI] User authentication and role-based authorization
- [AI] Email sending functionality through SMTP
- [AI] Responsive web interface with modern UI/UX
- [AI] Compliance validation workflow for generated content
- [AI] Performance under simulated load with multiple concurrent users
- [AI] Deployment to both local IIS and Azure App Service environments

## 5. Verification
<!-- >> This section provides the verification approaches and methods planned to qualify the software. The information items for verification are recommended to be given in a parallel manner with the requirement items in Section 3. The purpose of the verification process is to provide objective evidence that a system or system element fulfills its specified requirements and characteristics. -->
The system should develop layers incrementally starting in the following order:
- Create the databases, tables and sql accounts
- Create stored procedures for all CRUD operations required for each table
- Create services to host business logic and interact with backend database
- Create unit tests to test all code generated
- Create web application to call services
- Create functional tests to test major areas of functionality 

After each layer is created create an overview document and allow me to review prior to proceeding 

<!-- TODO: give more guidance, similar to section 3 -->
<!-- ieee 15288:2015 -->

## 6. Appendixes

 **Appendix A: Environment Variables**
 The following environment variables are required for system configuration:
 - OPENAI_API_KEY: OpenAI API key for AI email generation (no default for security reasons)
 - SQL_PASSWORD: Password for SQL Server SA account (no default for security reasons)
 - DB_SERVER: Database server hostname (default: localhost)
 - DB_NAME: Database name (default: CRMDb)
 - SMTP_SERVER: SMTP server for email sending (default: localhost)
 - SMTP_PORT: SMTP server port (default: 587)
 - ENVIRONMENT: Application environment (development/testing/production)
 - [AI] JWT_SECRET_KEY: Secret key for JWT token generation (no default for security)
 - [AI] SESSION_TIMEOUT: Session timeout in minutes (default: 30)
 - [AI] MAX_LOGIN_ATTEMPTS: Maximum failed login attempts before lockout (default: 5)
 - [AI] EMAIL_RATE_LIMIT: Maximum emails per hour per user (default: 100)
 - [AI] LOG_LEVEL: Logging level (default: Information)

 **Appendix B: Default User Accounts**
 The system includes the following default accounts for initial setup:
 - Username: admin, Password: admin123, Role: Administrator
 - This account should be used for initial system configuration only
 - Production deployments should change default passwords immediately

 **Appendix C: AI Email Types**
 The system supports the following AI-generated email types:
 - introduction: Initial contact emails to new prospects
 - follow_up: Follow-up emails after previous contact
 - promotional: Marketing and promotional content emails
 - meeting_request: Meeting scheduling and invitation emails

 **Appendix D: Compliance Features**
 The system implements the following compliance checks:
 - HIPAA validation for healthcare-related content
 - Microsoft Responsible AI principles validation
 - Content filtering for sensitive information detection
 - Audit logging for all email generation and sending activities

 **[AI] Appendix E: .NET Architecture Components**
 The system shall implement the following .NET-specific architecture:
 - [AI] Controllers: ASP.NET Core MVC controllers for handling HTTP requests
 - [AI] Services: Business logic services registered with dependency injection
 - [AI] Repositories: Data access repositories using Entity Framework Core
 - [AI] Models: Domain models and DTOs for data transfer
 - [AI] Middleware: Custom middleware for authentication, logging, and error handling
 - [AI] Configuration: Strongly-typed configuration classes bound to appsettings.json
 - [AI] Filters: Action filters for cross-cutting concerns like validation and logging

 **[AI] Appendix F: Database Migration Strategy**
 The system shall support database versioning and migrations:
 - [AI] Entity Framework Core Migrations for schema changes
 - [AI] Seed data scripts for initial system setup
 - [AI] Database rollback capabilities for failed deployments
 - [AI] Environment-specific data seeding (dev/test/prod)
 - [AI] Database backup and restore procedures
