from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Import all models here so they are registered with Base.metadata
from app.models.models import User, Company, Opportunity, Proposal, OpportunityDocument, ProposalSection, SectionTemplate, ProposalTeamMember, Subcontractor, ProposalSubcontractor, PricingData, Notification, Role, UserRole

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
