import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.models import User, Opportunity
from tests.test_main import test_db, client, override_get_db

def create_test_user_and_get_token():
    """Helper function to create a test user and get auth token"""
    # Create a test user in the database
    db = next(override_get_db())
    
    user = User(
        email="api_test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="API Test User",
        is_active=True,
        is_superuser=True  # Make superuser for full access
    )
    db.add(user)
    db.commit()
    
    # Login to get a token
    login_data = {
        "username": "api_test@example.com",
        "password": "testpassword"
    }
    
    login_response = client.post("/api/v1/auth/login", data=login_data)
    return login_response.json()["access_token"]

def test_create_opportunity(test_db):
    """Test creating a new opportunity"""
    token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    opportunity_data = {
        "title": "Test API Opportunity",
        "description": "An opportunity created through the API",
        "agency": "Test Agency",
        "solicitation_number": "API-TEST-001",
        "naics_code": "541512",
        "status": "active"
    }
    
    response = client.post(
        "/api/v1/opportunities/",
        headers=headers,
        json=opportunity_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == opportunity_data["title"]
    assert data["agency"] == opportunity_data["agency"]
    assert data["solicitation_number"] == opportunity_data["solicitation_number"]
    assert "id" in data

def test_get_opportunities(test_db):
    """Test getting a list of opportunities"""
    # Create a test opportunity
    db = next(override_get_db())
    opportunity = Opportunity(
        title="Test Get Opportunity",
        description="An opportunity for testing GET endpoint",
        agency="Test Agency",
        solicitation_number="GET-TEST-001",
        status="active"
    )
    db.add(opportunity)
    db.commit()
    
    # Get auth token
    token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test getting opportunities
    response = client.get("/api/v1/opportunities/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # Check if our test opportunity is in the list
    found = False
    for opp in data:
        if opp["title"] == "Test Get Opportunity":
            found = True
            assert opp["agency"] == "Test Agency"
            assert opp["solicitation_number"] == "GET-TEST-001"
    
    assert found is True

def test_get_opportunity_by_id(test_db):
    """Test getting a specific opportunity by ID"""
    # Create a test opportunity
    db = next(override_get_db())
    opportunity = Opportunity(
        title="Test Get By ID",
        description="An opportunity for testing GET by ID endpoint",
        agency="Test Agency",
        solicitation_number="GET-ID-TEST-001",
        status="active"
    )
    db.add(opportunity)
    db.commit()
    
    # Get auth token
    token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test getting opportunity by ID
    response = client.get(f"/api/v1/opportunities/{opportunity.id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Get By ID"
    assert data["agency"] == "Test Agency"
    assert data["solicitation_number"] == "GET-ID-TEST-001"
    assert data["id"] == opportunity.id

def test_update_opportunity(test_db):
    """Test updating an opportunity"""
    # Create a test opportunity
    db = next(override_get_db())
    opportunity = Opportunity(
        title="Test Update Opportunity",
        description="An opportunity for testing UPDATE endpoint",
        agency="Old Agency",
        solicitation_number="UPDATE-TEST-001",
        status="active"
    )
    db.add(opportunity)
    db.commit()
    
    # Get auth token
    token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Update data
    update_data = {
        "title": "Updated Opportunity",
        "agency": "New Agency"
    }
    
    # Test updating opportunity
    response = client.put(
        f"/api/v1/opportunities/{opportunity.id}",
        headers=headers,
        json=update_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Opportunity"
    assert data["agency"] == "New Agency"
    assert data["solicitation_number"] == "UPDATE-TEST-001"  # Unchanged field
    
    # Verify in database
    db = next(override_get_db())
    updated_opp = db.query(Opportunity).filter(Opportunity.id == opportunity.id).first()
    assert updated_opp.title == "Updated Opportunity"
    assert updated_opp.agency == "New Agency"

def test_delete_opportunity(test_db):
    """Test deleting an opportunity"""
    # Create a test opportunity
    db = next(override_get_db())
    opportunity = Opportunity(
        title="Test Delete Opportunity",
        description="An opportunity for testing DELETE endpoint",
        agency="Test Agency",
        status="active"
    )
    db.add(opportunity)
    db.commit()
    opp_id = opportunity.id
    
    # Get auth token
    token = create_test_user_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test deleting opportunity
    response = client.delete(f"/api/v1/opportunities/{opp_id}", headers=headers)
    
    assert response.status_code == 200
    
    # Verify it's deleted from database
    db = next(override_get_db())
    deleted_opp = db.query(Opportunity).filter(Opportunity.id == opp_id).first()
    assert deleted_opp is None
