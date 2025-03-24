# GovBid Pro - Development Guide

This document provides information for developers who want to contribute to or extend the Python version of GovBid Pro.

## Development Environment Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Your favorite code editor or IDE (VS Code, PyCharm, etc.)
- Docker (optional, for containerized development)

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/your-organization/govbid-pro-python.git
cd govbid-pro-python
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

4. Set up pre-commit hooks:
```bash
pre-commit install
```

### Code Style and Linting

This project follows the PEP 8 style guide and uses the following tools for code quality:

- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

Run all checks with:
```bash
# Format code
black app tests
isort app tests

# Check code
flake8 app tests
mypy app tests
```

## Project Architecture

### Overview

GovBid Pro follows a layered architecture:

1. **Presentation Layer**: FastAPI routes and Jinja2 templates
2. **Business Logic Layer**: Services and utilities
3. **Data Access Layer**: SQLAlchemy models and repositories

### Key Components

- **FastAPI Application**: Defined in `app/main.py`
- **API Routes**: Defined in `app/api/api_v1/endpoints/`
- **Web Routes**: Defined in `app/web/routes.py`
- **Database Models**: Defined in `app/models/models.py`
- **Pydantic Schemas**: Defined in `app/schemas/schemas.py`
- **Business Logic**: Implemented in `app/services/`
- **Authentication**: Implemented in `app/core/security.py` and `app/api/deps.py`

### Dependency Injection

FastAPI's dependency injection system is used throughout the application:

```python
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.models import User

router = APIRouter()

@router.get("/items/")
def read_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Implementation
    pass
```

## Database

### Models

SQLAlchemy models are defined in `app/models/models.py`. Key models include:

- `User`: Application users
- `Company`: Organizations using the system
- `Opportunity`: Government contract opportunities
- `Proposal`: Responses to opportunities

### Migrations

Database migrations are managed using Alembic:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Run migrations
alembic upgrade head

# Downgrade one version
alembic downgrade -1
```

### Relationships

The database schema includes several relationships:

- One-to-many: Company to Users, Opportunity to Proposals
- Many-to-many: Proposals to Subcontractors (via junction table)

## Authentication and Authorization

### JWT Authentication

The application uses JWT tokens for authentication:

1. User logs in with email/password
2. Server validates credentials and returns a JWT token
3. Client includes token in Authorization header for subsequent requests
4. Server validates token and identifies the user

### Role-Based Access Control

Access control is implemented using roles and permissions:

- `is_superuser` flag for admin access
- Role-based permissions stored in the `roles` table
- User-role assignments in the `user_roles` table

## Testing

### Test Structure

Tests are organized in the `tests/` directory:

- `tests/test_main.py`: Application setup tests
- `tests/test_models.py`: Database model tests
- `tests/test_auth.py`: Authentication tests
- `tests/test_*_api.py`: API endpoint tests

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_models.py

# Run with coverage
pytest --cov=app

# Generate coverage report
pytest --cov=app --cov-report=html
```

### Test Database

Tests use a separate SQLite database to avoid affecting development data.

## Frontend Development

### Templates

Jinja2 templates are located in `app/web/templates/`:

- `base.html`: Base template with common layout
- Other templates extend the base template

### Static Files

CSS, JavaScript, and other static files are in `app/web/static/`:

- `css/styles.css`: Custom styles
- `js/main.js`: Common JavaScript functions

### JavaScript

The frontend uses vanilla JavaScript with fetch API for AJAX requests:

```javascript
async function fetchData(url) {
    const token = localStorage.getItem('token');
    const response = await fetch(url, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.json();
}
```

## Deployment

### Docker Deployment

A Dockerfile is provided for containerized deployment:

```bash
# Build the Docker image
docker build -t govbid-pro .

# Run the container
docker run -p 8000:8000 govbid-pro
```

### Environment Variables

Configure the application using environment variables:

- `SECRET_KEY`: JWT secret key
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Production Considerations

For production deployment:

1. Use a production-grade database (PostgreSQL recommended)
2. Set up HTTPS with a valid SSL certificate
3. Configure proper logging
4. Use a process manager (systemd, supervisor, etc.)
5. Set up monitoring and alerting

## Adding New Features

### Adding a New API Endpoint

1. Create a new file in `app/api/api_v1/endpoints/` or add to an existing one
2. Define the route and implementation
3. Include the router in `app/api/api_v1/api.py`
4. Add appropriate tests in `tests/`

### Adding a New Database Model

1. Define the model in `app/models/models.py`
2. Create corresponding Pydantic schemas in `app/schemas/schemas.py`
3. Create a migration: `alembic revision --autogenerate -m "Add new model"`
4. Add tests for the new model

### Adding a New Web Page

1. Create a new template in `app/web/templates/`
2. Add a route in `app/web/routes.py`
3. Update navigation in `base.html` if needed

## Troubleshooting Development Issues

### Common Issues

1. **Import errors**: Check your Python path and virtual environment
2. **Database errors**: Verify connection string and run migrations
3. **Authentication issues**: Check token generation and validation
4. **CORS errors**: Verify CORS settings for frontend development

### Debugging

- Use FastAPI's automatic documentation at `/docs` to test API endpoints
- Enable debug logging: `LOG_LEVEL=DEBUG uvicorn app.main:app --reload`
- Use Python debugger: `import pdb; pdb.set_trace()`

## Performance Optimization

- Use database indexes for frequently queried fields
- Implement caching for expensive operations
- Use async endpoints for I/O-bound operations
- Optimize database queries (use `.select_from()` and `.options()`)

## Security Best Practices

- Keep dependencies updated
- Use parameterized queries to prevent SQL injection
- Validate all user input
- Implement proper error handling
- Use HTTPS in production
- Follow the principle of least privilege for database access
- Regularly audit authentication and authorization code
