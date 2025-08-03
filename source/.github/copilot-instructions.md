<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# MyCRM Project Instructions

This is a Python CherryPy web application for customer relationship management with AI-powered email generation.

## Architecture Guidelines

- Use **Repository Pattern** with automatic fallback from SQL Server to mock data
- Implement **Factory Pattern** for repository creation
- Follow **MVC Architecture** with clear separation of concerns
- Use **Service Layer** for business logic centralization
- Apply **Dependency Injection** for loose coupling

## Code Standards

- All database queries must use parameterized queries to prevent SQL injection
- Passwords must be hashed using bcrypt
- Environment variables should be used for all sensitive configuration
- Include comprehensive error handling and logging
- Follow PEP 8 style guidelines for Python code

## Security Requirements

- Implement session-based authentication
- Support role-based authorization (Administrator/Standard User)
- Store no passwords in code - use environment variables
- Include HIPAA compliance considerations for healthcare deployment
- Validate all user inputs

## Testing Requirements

- Write unit tests for all business logic
- Include functional tests for end-to-end scenarios
- Test both SQL Server and mock data scenarios
- Achieve high code coverage

## AI Integration

- Use OpenAI GPT-3.5 for email personalization
- Include responsible AI principle validation
- Implement configurable compliance checking
- Handle AI service unavailability gracefully

When generating code, prioritize security, maintainability, and adherence to the multi-layer architecture pattern described in the requirements.
