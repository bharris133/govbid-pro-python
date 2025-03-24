# GovBid Pro - Python Version Setup Guide

This guide provides detailed instructions for setting up and running the Python version of GovBid Pro.

## Detailed Installation Steps

### System Requirements

- Python 3.10 or higher
- pip (Python package installer)
- Git (for cloning the repository)
- 2GB RAM minimum (4GB recommended)
- 1GB free disk space

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-organization/govbid-pro-python.git
cd govbid-pro-python
```

### Step 2: Set Up Virtual Environment

Creating a virtual environment isolates the application dependencies from your system Python installation.

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` appear at the beginning of your command prompt, indicating the virtual environment is active.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- FastAPI
- SQLAlchemy
- Pydantic
- Jinja2
- python-jose (for JWT)
- passlib (for password hashing)
- uvicorn (ASGI server)
- pytest (for testing)

### Step 4: Configure the Application

1. Create a `.env` file in the root directory:

```
SECRET_KEY=your-secret-key-here
SQLALCHEMY_DATABASE_URI=sqlite:///./govbid_pro.db
ACCESS_TOKEN_EXPIRE_MINUTES=11520  # 8 days
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=change-this-password
```

For production, it's recommended to use a more secure database like PostgreSQL:

```
SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/govbid_pro
```

### Step 5: Initialize the Database

```bash
python -m app.db.init_db
```

This script will:
- Create all database tables
- Set up initial data if needed
- Create the first superuser account using credentials from your `.env` file

### Step 6: Verify Installation

Run the tests to ensure everything is working correctly:

```bash
pytest
```

All tests should pass, indicating that the application is properly set up.

## Running the Application

### Development Mode

For development with automatic reloading:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

For production deployment:

```bash
# Using Gunicorn with multiple workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app

# Or using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Accessing the Application

- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative API Documentation: http://localhost:8000/redoc

## Default Credentials

The application is initialized with a default superuser account:
- Email: admin@example.com (or the value of FIRST_SUPERUSER in your .env file)
- Password: The value of FIRST_SUPERUSER_PASSWORD in your .env file

**Important:** Change these credentials immediately after first login.

## Database Management

### Backup Database

For SQLite:
```bash
cp govbid_pro.db govbid_pro_backup.db
```

For PostgreSQL:
```bash
pg_dump -U username -d govbid_pro > govbid_pro_backup.sql
```

### Restore Database

For SQLite:
```bash
cp govbid_pro_backup.db govbid_pro.db
```

For PostgreSQL:
```bash
psql -U username -d govbid_pro < govbid_pro_backup.sql
```

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Verify database URI in .env file
   - Ensure database server is running (for PostgreSQL/MySQL)
   - Check permissions on the database file (for SQLite)

2. **Package import errors**
   - Ensure virtual environment is activated
   - Verify all dependencies are installed: `pip install -r requirements.txt`

3. **Permission errors**
   - Check file permissions for database and log files
   - Ensure the application has write access to necessary directories

4. **Port already in use**
   - Change the port: `uvicorn app.main:app --port 8080`
   - Find and stop the process using the port: `lsof -i :8000` then `kill <PID>`

### Getting Help

If you encounter issues not covered in this guide, please:
1. Check the logs in the `logs` directory
2. Review the API documentation for endpoint details
3. Contact support at [your-support-email]

## Upgrading

To upgrade to a newer version:

1. Backup your database
2. Pull the latest code: `git pull origin main`
3. Activate your virtual environment
4. Update dependencies: `pip install -r requirements.txt`
5. Run database migrations if available: `python -m app.db.run_migrations`
6. Restart the application

## Security Recommendations

1. Change the default superuser password immediately
2. Use a strong, unique SECRET_KEY
3. In production, use HTTPS with a valid SSL certificate
4. Regularly update dependencies to patch security vulnerabilities
5. Implement proper backup procedures for your database
