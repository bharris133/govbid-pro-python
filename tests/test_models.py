import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.security import get_password_hash, verify_password
from app.db.base_class import Base
from app.models.models import User, Company, Opportunity, Proposal

# Create a separate test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Create session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """Fixture that returns a SQLAlchemy session with tables created"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

def test_password_hashing():
    """Test that password hashing and verification works correctly"""
    password = "testpassword123"
    hashed_password = get_password_hash(password)
    
    # Hashed password should be different from original
    assert hashed_password != password
    
    # Verification should work
    assert verify_password(password, hashed_password) is True
    
    # Wrong password should fail verification
    assert verify_password("wrongpassword", hashed_password) is False

def test_user_model(db_session):
    """Test creating and querying a user"""
    # Create a test company
    company = Company(
        name="Test Company",
        description="A company for testing",
        website="https://testcompany.com"
    )
    db_session.add(company)
    db_session.commit()
    
    # Create a test user
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        is_active=True,
        company_id=company.id
    )
    db_session.add(user)
    db_session.commit()
    
    # Query the user
    db_user = db_session.query(User).filter(User.email == "test@example.com").first()
    
    # Check that the user was created correctly
    assert db_user is not None
    assert db_user.email == "test@example.com"
    assert db_user.full_name == "Test User"
    assert db_user.is_active is True
    assert db_user.company_id == company.id
    
    # Check relationship with company
    assert db_user.company.name == "Test Company"

def test_opportunity_model(db_session):
    """Test creating and querying an opportunity"""
    # Create a test opportunity
    opportunity = Opportunity(
        title="Test Opportunity",
        description="An opportunity for testing",
        agency="Test Agency",
        solicitation_number="TEST-2025-001",
        naics_code="541512",
        status="active"
    )
    db_session.add(opportunity)
    db_session.commit()
    
    # Query the opportunity
    db_opportunity = db_session.query(Opportunity).filter(Opportunity.title == "Test Opportunity").first()
    
    # Check that the opportunity was created correctly
    assert db_opportunity is not None
    assert db_opportunity.title == "Test Opportunity"
    assert db_opportunity.agency == "Test Agency"
    assert db_opportunity.solicitation_number == "TEST-2025-001"
    assert db_opportunity.status == "active"

def test_proposal_model(db_session):
    """Test creating and querying a proposal with relationships"""
    # Create a test company
    company = Company(
        name="Test Company",
        description="A company for testing"
    )
    db_session.add(company)
    db_session.commit()
    
    # Create a test user
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        company_id=company.id
    )
    db_session.add(user)
    db_session.commit()
    
    # Create a test opportunity
    opportunity = Opportunity(
        title="Test Opportunity",
        agency="Test Agency",
        status="active"
    )
    db_session.add(opportunity)
    db_session.commit()
    
    # Create a test proposal
    proposal = Proposal(
        title="Test Proposal",
        company_id=company.id,
        created_by_id=user.id,
        opportunity_id=opportunity.id,
        status="draft"
    )
    db_session.add(proposal)
    db_session.commit()
    
    # Query the proposal
    db_proposal = db_session.query(Proposal).filter(Proposal.title == "Test Proposal").first()
    
    # Check that the proposal was created correctly
    assert db_proposal is not None
    assert db_proposal.title == "Test Proposal"
    assert db_proposal.status == "draft"
    
    # Check relationships
    assert db_proposal.company.name == "Test Company"
    assert db_proposal.created_by.email == "test@example.com"
    assert db_proposal.opportunity.title == "Test Opportunity"
