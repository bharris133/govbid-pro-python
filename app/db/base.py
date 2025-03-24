from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base_class import Base

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import all models here so they are registered with Base.metadata
from app.models.models import User, Company, Opportunity, Proposal, OpportunityDocument, ProposalSection, SectionTemplate, ProposalTeamMember, Subcontractor, ProposalSubcontractor, PricingData, Notification, Role, UserRole
