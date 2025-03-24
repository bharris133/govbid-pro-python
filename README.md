# GovBid Pro - Python Version

GovBid Pro is a SaaS web application for government contractors to respond to RFPs, RFIs, and procurement requests from government agencies. This Python version has been converted from the original Next.js/React implementation to use a modern Python tech stack.

## Technology Stack

- **Backend Framework**: FastAPI
- **Database ORM**: SQLAlchemy
- **Database**: SQLite (can be easily configured for PostgreSQL or other databases)
- **Authentication**: JWT (JSON Web Tokens)
- **Frontend Templating**: Jinja2
- **CSS Framework**: Bootstrap 5
- **Testing**: pytest

## Features

- User authentication and authorization
- Company and user management
- Opportunity tracking and management
- Proposal development and collaboration
- Subcontractor search and management
- Pricing research based on historical contract data
- Formatting requirements identification
- Data privacy and security options

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Setup Steps

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

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python -m app.db.init_db
```

5. Create initial superuser (optional):
```bash
python -m app.db.create_superuser
```

## Running the Application

### Development Server

To run the development server:

```bash
uvicorn app.main:app --reload
```

The application will be available at http://localhost:8000

### Production Deployment

For production deployment, it's recommended to use Gunicorn as a WSGI server:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

To run the tests:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=app
```

## Project Structure

```
govbid-pro-python/
├── app/                    # Main application package
│   ├── api/                # API endpoints
│   │   └── api_v1/         # API version 1
│   │       └── endpoints/  # API endpoint modules
│   ├── core/               # Core functionality
│   ├── db/                 # Database setup and models
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic services
│   ├── utils/              # Utility functions
│   ├── web/                # Web interface
│   │   ├── static/         # Static files (CSS, JS)
│   │   └── templates/      # Jinja2 templates
│   └── main.py             # Application entry point
├── tests/                  # Test modules
├── docs/                   # Documentation
├── requirements.txt        # Dependencies
└── README.md               # Project overview
```

## Configuration

Application configuration is managed through environment variables and the `app/core/config.py` file. Key configuration options include:

- `SECRET_KEY`: Used for JWT token generation
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time
- `CORS_ORIGINS`: Allowed CORS origins

## User Guide

### Authentication

1. Navigate to the login page at `/login`
2. Enter your email and password
3. Upon successful login, you'll be redirected to the dashboard

### Dashboard

The dashboard provides an overview of:
- Active opportunities
- Draft proposals
- Upcoming deadlines
- Recent activity

### Opportunities

The opportunities page allows you to:
- View all opportunities
- Add new opportunities
- Filter and search opportunities
- View opportunity details

### Proposals

The proposals page allows you to:
- Create new proposals
- Manage existing proposals
- Track proposal status
- Collaborate with team members

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

[Specify the license here]

## Support

For support, please contact [your contact information]
