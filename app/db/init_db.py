import logging
import os
from sqlalchemy.orm import Session

from app.db.base import engine, get_db
from app.models.models import Base, User, Company, Role, UserRole
from app.core.config import settings
from app.core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db() -> None:
    # Create database file directory if it doesn't exist
    db_file = settings.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
    os.makedirs(os.path.dirname(os.path.abspath(db_file)), exist_ok=True)
    
    # Create tables
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")
    
    # Create initial data
    db = next(get_db())
    create_initial_data(db)
    logger.info("Initial data created successfully.")

def create_initial_data(db: Session) -> None:
    # Check if we already have users
    try:
        user = db.query(User).first()
        if user:
            logger.info("Database already initialized, skipping initial data creation.")
            return
    except Exception as e:
        logger.error(f"Error checking for existing users: {e}")
        # Continue with initialization even if check fails
    
    # Create default company
    company = Company(
        name="Default Company",
        description="Default company for initial setup",
        website="https://example.com"
    ) 
    db.add(company)
    db.commit()
    db.refresh(company)
    logger.info(f"Created default company: {company.name}")
    
    # Create admin role
    admin_role = Role(
        name="admin",
        description="Administrator with full access",
        permissions={"admin": True, "user": True}
    )
    db.add(admin_role)
    
    # Create user role
    user_role = Role(
        name="user",
        description="Regular user with limited access",
        permissions={"user": True}
    )
    db.add(user_role)
    db.commit()
    logger.info("Created roles: admin, user")
    
    # Create first superuser
    superuser = User(
        email=settings.FIRST_SUPERUSER,
        hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
        full_name="Initial Admin",
        is_active=True,
        is_superuser=True,
        company_id=company.id
    )
    db.add(superuser)
    db.commit()
    db.refresh(superuser)
    logger.info(f"Created superuser: {superuser.email}")
    
    # Assign admin role to superuser
    user_role = UserRole(
        user_id=superuser.id,
        role_id=admin_role.id
    )
    db.add(user_role)
    db.commit()
    logger.info(f"Assigned admin role to superuser: {superuser.email}")

if __name__ == "__main__":
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialization completed.")
