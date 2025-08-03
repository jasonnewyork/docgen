# MyCRM - Customer Relationship Management System

A modern web-based CRM application built with Python and CherryPy, featuring AI-powered email generation and multi-tier architecture.

## Features

- **Customer Management**: Complete CRUD operations for customer data
- **AI Email Generation**: OpenAI-powered personalized email creation
- **User Management**: Role-based access control (Administrator/Standard User)
- **Adaptive Architecture**: Automatic fallback from SQL Server to mock data
- **Security**: HIPAA compliance considerations and secure authentication
- **Testing**: Comprehensive unit and functional test coverage

## Architecture

- **Presentation Layer**: HTML templates, CSS, JavaScript
- **Web Application Layer**: CherryPy framework, controllers, routing
- **Business Logic Layer**: Service classes, validation, error handling
- **Data Access Layer**: Repository pattern with factory for switching
- **Data Persistence**: SQL Server database and mock implementations

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   
   **SECURITY NOTE**: Never commit credentials to source control.
   
   **Copy the environment template:**
   ```bash
   copy .env.template .env
   ```
   
   **Edit .env file with your actual credentials:**
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SQL_PASSWORD=your_sql_server_password_here
   ```
   
   **Alternative - Set directly in PowerShell:**
   ```bash
   $env:OPENAI_API_KEY="your_openai_api_key"
   $env:SQL_PASSWORD="your_sql_password"
   ```

3. **Run Database Setup** (optional - will fallback to mock data if SQL Server unavailable):
   ```bash
   python scripts/setup_database.py
   ```

4. **Start the Application**:
   ```bash
   python app.py
   ```

5. **Access the Application**:
   - Open browser to `http://localhost:8080`
   - Default admin login: `admin` / `admin123`

## Project Structure

```
mycrm/
├── app.py                 # Main CherryPy application entry point
├── config/
│   ├── __init__.py
│   ├── database.py        # Database configuration
│   └── settings.py        # Application settings
├── data/
│   ├── __init__.py
│   ├── models/            # Data models
│   ├── repositories/      # Repository pattern implementations
│   └── factory.py         # Repository factory
├── business/
│   ├── __init__.py
│   └── services/          # Business logic services
├── web/
│   ├── __init__.py
│   ├── controllers/       # Web controllers
│   ├── templates/         # HTML templates
│   └── static/           # CSS, JS, images
├── scripts/
│   ├── setup_database.py  # Database setup script
│   └── sql/               # SQL scripts
├── tests/
│   ├── unit/              # Unit tests
│   └── functional/        # End-to-end tests
└── requirements.txt       # Python dependencies
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for email generation
- `SQL_PASSWORD`: SQL Server SA account password
- `DATABASE_URL`: Optional custom database connection string
- `ENVIRONMENT`: Set to 'development', 'testing', or 'production'

## Security Considerations

### Environment Variables
- **Never commit credentials to source control**
- Use `.env` file for local development (included in `.gitignore`)
- Set environment variables directly on production servers
- Required variables: `OPENAI_API_KEY`, `SQL_PASSWORD`

### Database Security
- Passwords are hashed using bcrypt before storage
- Session-based authentication with secure token generation
- SQL injection protection through parameterized queries
- Connection strings use environment variables only

### Production Deployment
- Change default admin password immediately
- Use HTTPS in production
- Set strong SQL Server passwords
- Regularly rotate API keys and passwords

## Testing

Run unit tests:
```bash
pytest tests/unit/ -v
```

Run functional tests:
```bash
pytest tests/functional/ -v
```

Run all tests with coverage:
```bash
pytest --cov=. --cov-report=html
```

## Development Notes

- The system automatically detects SQL Server availability and falls back to mock data
- All passwords are securely hashed using bcrypt
- Email compliance checking is configurable for different industries
- The application supports both local and Azure deployment

## License

This project is licensed under the MIT License.
