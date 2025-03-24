import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.models import User, Company, Proposal, Opportunity
from tests.test_main import test_db, client, override_get_db
from tests.test_opportunities_api import create_test_user_and_get_token

def test_create_proposal(test_db):
    """Test creating a new proposal"""
    # Create test company and opportunity
    db = next(override_get_db())
    
    company = Company(
        name="Test API Company",
        description="A company for testing API"
    )
    db.add(company)
    db.commit()
    
    opportunity = Opportunity(
        title="Test Proposal Opportunity",
        agency="Test Agency",
        status="active"
    )
    db.add(opportunity)
    db.commit()
    
    # Get auth token
    token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    proposal_data = {
        "title": "Test API Proposal",
        "opportunity_id": opportunity.id,
        "company_id": company.id,
        "status": "draft"
    }
    
    response = client.post(
        "/api/v1/proposals/",
        headers=headers,
        json=proposal_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == proposal_data["title"]
    assert data["opportunity_id"] == proposal_data["opportunity_id"]
    assert data["company_id"] == proposal_data["company_id"]
    assert data["status"] == proposal_data["status"]
    assert "id" in data

def test_get_proposals(test_db):
    """Test getting a list of proposals"""
    # Create test user, company, opportunity, and proposal
    db = next(override_get_db())
    
    user = User(
        email="proposal_test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Proposal Test User",
        is_active=True
    )
    db.add(user)
    db.commit()
    
    company = Company(
        name="Test Proposal Company",
        description="A company for testing proposals"
    )
    db.add(company)
    db.commit()
    
    opportunity = Opportunity(
        title="Test Proposal Opportunity",
        agency="Test Agency",
        status="active"
    )
    db.add(opportunity)
    db.commit()
    
    proposal = Proposal(
        title="Test Get Proposal",
        opportunity_id=opportunity.id,
        company_id=company.id,
        created_by_id=user.id,
        status="draft"
    )
    db.add(proposal)
    db.commit()
    
    # Get auth token
    token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test getting proposals
    response = client.get("/api/v1/proposals/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # Check if our test proposal is in the list
    found = False
    for prop in data:
        if prop["title"] == "Test Get Proposal":
            found = True
            assert prop["company_id"] == company.id
            assert prop["opportunity_id"] == opportunity.id
            assert prop["status"] == "draft"
    
    assert found is True

def test_get_proposal_by_id(test_db):
    """Test getting a specific proposal by ID"""
    # Create test user, company, opportunity, and proposal
    db = next(override_get_db())
    
    user = User(
        email="proposal_get_test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Proposal Get Test User",
        is_active=True
    )
    db.add(user)
    db.commit()
    
    company = Company(
        name="Test Get Proposal Company",
        description="A company for testing get proposal"
    )
    db.add(company)
    db.commit()
    
    opportunity = Opportunity(
        title="Test Get Proposal Opportunity",
        agency="Test Agency",
        status="active"
    )
    db.add(opportunity)
    db.commit()
    
    proposal = Proposal(
        title="Test Get Proposal By ID",
        opportunity_id=opportunity.id,
        company_id=company.id,
        created_by_id=user.id,
        status="draft"
    )
    db.add(proposal)
    db.commit()
    
    # Get auth token
    token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test getting proposal by ID
    response = client.get(f"/api/v1/proposals/{proposal.id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Get Proposal By ID"
    assert data["company_id"] == company.id
    assert data["opportunity_id"] == opportunity.id
    assert data["status"] == "draft"
    assert data["id"] == proposal.id

def test_update_proposal(test_db):
    """Test updating a proposal"""
    # Create test user, company, opportunity, and proposal
    db = next(override_get_db())
    
    user = User(
        email="proposal_update_test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Proposal Update Test User",
        is_active=True
    )
    db.add(user)
    db.commit()
    
    company = Company(
        name="Test Update Proposal Company",
        description="A company for testing update proposal"
    )
    db.add(company)
    db.commit()
    
    opportunity = Opportunity(
        title="Test Update Proposal Opportunity",
        agency="Test Agency",
        status="active"
    )
    db.add(opportunity)
    db.commit()
    
    proposal = Proposal(
        title="Test Update Proposal",
        opportunity_id=opportunity.id,
        company_id=company.id,
        created_by_id=user.id,
        status="draft"
    )
    db.add(proposal)
    db.commit()
    
    # Get auth token
    token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Update data
    update_data = {
        "title": "Updated Proposal Title",
        "status": "in_progress"
    }
    
    # Test updating proposal
    response = client.put(
        f"/api/v1/proposals/{proposal.id}",
        headers=headers,
        json=update_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Proposal Title"
    assert data["status"] == "in_progress"
    assert data["company_id"] == company.id  # Unchanged field
    
    # Verify in database
    db = next(override_get_db())
    updated_proposal = db.query(Proposal).filter(Proposal.id == proposal.id).first()
    assert updated_proposal.title == "Updated Proposal Title"
    assert updated_proposal.status == "in_progress"

def test_delete_proposal(test_db):
    """Test deleting a proposal"""
    # Create test user, company, opportunity, and proposal
    db = next(override_get_db())
    
    user = User(
        email="proposal_delete_test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Proposal Delete Test User",
        is_active=True
    )
    db.add(user)
    db.commit()
    
    company = Company(
        name="Test Delete Proposal Company",
        description="A company for testing delete proposal"
    )
    db.add(company)
    db.commit()
    
    opportunity = Opportunity(
        title="Test Delete Proposal Opportunity",
        agency="Test Agency",
        status="active"
    )
    db.add(opportunity)
    db.commit()
    
    proposal = Proposal(
        title="Test Delete Proposal",
        opportunity_id=opportunity.id,
        company_id=company.id,
        created_by_id=user.id,
        status="draft"
    )
    db.add(proposal)
    db.commit()
    proposal_id = proposal.id
    
    # Get auth token
    token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test deleting proposal
    response = client.delete(f"/api/v1/proposals/{proposal_id}", headers=headers)
    
    assert response.status_code == 200
    
    # Verify it's deleted from database
    db = next(override_get_db())
    deleted_proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    assert deleted_proposal is None
