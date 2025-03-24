import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.models import User, Company
from tests.test_main import test_db, client, override_get_db

def test_login_access_token(test_db):
    """Test login endpoint with valid credentials"""
    # Create a test user in the database
    db = next(override_get_db())
    
    user = User(
        email="auth_test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Auth Test User",
        is_active=True
    )
    db.add(user)
    db.commit()
    
    # Test login with valid credentials
    login_data = {
        "username": "auth_test@example.com",
        "password": "testpassword"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_login_invalid_credentials(test_db):
    """Test login endpoint with invalid credentials"""
    # Test login with invalid credentials
    login_data = {
        "username": "auth_test@example.com",
        "password": "wrongpassword"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_get_current_user(test_db):
    """Test getting current user information with valid token"""
    # Create a test user in the database
    db = next(override_get_db())
    
    user = User(
        email="current_user_test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Current User Test",
        is_active=True
    )
    db.add(user)
    db.commit()
    
    # Login to get a token
    login_data = {
        "username": "current_user_test@example.com",
        "password": "testpassword"
    }
    
    login_response = client.post("/api/v1/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    
    # Test getting current user with valid token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == "current_user_test@example.com"
    assert user_data["full_name"] == "Current User Test"
    assert user_data["is_active"] is True

def test_get_current_user_invalid_token(test_db):
    """Test getting current user information with invalid token"""
    # Test with invalid token
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == 403
    assert "Could not validate credentials" in response.json()["detail"]
