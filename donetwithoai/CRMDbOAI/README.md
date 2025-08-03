# MyCRM ASP.NET Core MVC Application

This project is an enterprise-grade CRM web application built with ASP.NET Core MVC, Entity Framework Core (database-first), and SQL Server. It connects to an existing CRMDb database on localhost using the SA account and password from the SQL_PASSWORD environment variable.

## Features
- Customer and user management (CRUD)
- Role-based authentication and authorization
- AI-powered email generation and compliance checks
- Audit logging and health monitoring
- Responsive web UI

## Getting Started
1. Ensure SQL Server is running and CRMDb is accessible on localhost.
2. Set the SQL_PASSWORD environment variable with the SA password.
3. Build and run the application using Visual Studio or `dotnet` CLI.

## Requirements
See `requirements.md` for full specification and architecture details.

## Environment Variables
- SQL_PASSWORD: SA account password
- OPENAI_API_KEY: OpenAI API key
- See requirements.md for all required variables.

## Development
- .NET 9
- Entity Framework Core (database-first)
- ASP.NET Core MVC

## License
MIT
