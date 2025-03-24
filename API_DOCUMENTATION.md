# GovBid Pro - API Documentation

This document provides detailed information about the API endpoints available in the Python version of GovBid Pro.

## Authentication

### Login

```
POST /api/v1/auth/login
```

Authenticates a user and returns an access token.

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "userpassword"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User

```
GET /api/v1/auth/me
```

Returns information about the currently authenticated user.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "User Name",
  "is_active": true,
  "company_id": 1,
  "created_at": "2025-03-24T00:00:00"
}
```

## Users

### Create User

```
POST /api/v1/users/
```

Creates a new user. Requires admin privileges.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "password": "newuserpassword",
  "full_name": "New User",
  "company_id": 1
}
```

**Response:**
```json
{
  "id": 2,
  "email": "newuser@example.com",
  "full_name": "New User",
  "is_active": true,
  "company_id": 1,
  "created_at": "2025-03-24T00:00:00"
}
```

### Get Users

```
GET /api/v1/users/
```

Returns a list of users. Requires admin privileges.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "full_name": "User Name",
    "is_active": true,
    "company_id": 1,
    "created_at": "2025-03-24T00:00:00"
  },
  {
    "id": 2,
    "email": "newuser@example.com",
    "full_name": "New User",
    "is_active": true,
    "company_id": 1,
    "created_at": "2025-03-24T00:00:00"
  }
]
```

### Get User by ID

```
GET /api/v1/users/{user_id}
```

Returns information about a specific user.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "User Name",
  "is_active": true,
  "company_id": 1,
  "created_at": "2025-03-24T00:00:00"
}
```

### Update User

```
PUT /api/v1/users/{user_id}
```

Updates a user's information.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "full_name": "Updated User Name",
  "password": "newpassword"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Updated User Name",
  "is_active": true,
  "company_id": 1,
  "created_at": "2025-03-24T00:00:00"
}
```

## Companies

### Create Company

```
POST /api/v1/companies/
```

Creates a new company.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "name": "New Company",
  "description": "Company description",
  "website": "https://example.com",
  "address": "123 Main St, City, State, ZIP",
  "phone": "555-123-4567",
  "email": "contact@example.com",
  "naics_codes": "541512,541511"
}
```

**Response:**
```json
{
  "id": 2,
  "name": "New Company",
  "description": "Company description",
  "website": "https://example.com",
  "address": "123 Main St, City, State, ZIP",
  "phone": "555-123-4567",
  "email": "contact@example.com",
  "naics_codes": "541512,541511",
  "created_at": "2025-03-24T00:00:00"
}
```

### Get Companies

```
GET /api/v1/companies/
```

Returns a list of companies.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Existing Company",
    "description": "Existing company description",
    "website": "https://existing.com",
    "created_at": "2025-03-23T00:00:00"
  },
  {
    "id": 2,
    "name": "New Company",
    "description": "Company description",
    "website": "https://example.com",
    "address": "123 Main St, City, State, ZIP",
    "phone": "555-123-4567",
    "email": "contact@example.com",
    "naics_codes": "541512,541511",
    "created_at": "2025-03-24T00:00:00"
  }
]
```

## Opportunities

### Create Opportunity

```
POST /api/v1/opportunities/
```

Creates a new opportunity.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title": "IT Support Services",
  "description": "Providing IT support services for government agency",
  "agency": "Department of Defense",
  "solicitation_number": "DOD-2025-IT-001",
  "naics_code": "541512",
  "posted_date": "2025-03-15T00:00:00",
  "due_date": "2025-04-15T00:00:00",
  "url": "https://sam.gov/opportunity/123456",
  "status": "active",
  "estimated_value": 500000
}
```

**Response:**
```json
{
  "id": 1,
  "title": "IT Support Services",
  "description": "Providing IT support services for government agency",
  "agency": "Department of Defense",
  "solicitation_number": "DOD-2025-IT-001",
  "naics_code": "541512",
  "posted_date": "2025-03-15T00:00:00",
  "due_date": "2025-04-15T00:00:00",
  "url": "https://sam.gov/opportunity/123456",
  "status": "active",
  "estimated_value": 500000,
  "created_at": "2025-03-24T00:00:00"
}
```

### Get Opportunities

```
GET /api/v1/opportunities/
```

Returns a list of opportunities.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `status` (optional): Filter by status (active, archived, etc.)
- `agency` (optional): Filter by agency
- `naics_code` (optional): Filter by NAICS code

**Response:**
```json
[
  {
    "id": 1,
    "title": "IT Support Services",
    "agency": "Department of Defense",
    "solicitation_number": "DOD-2025-IT-001",
    "due_date": "2025-04-15T00:00:00",
    "status": "active",
    "created_at": "2025-03-24T00:00:00"
  }
]
```

### Get Opportunity by ID

```
GET /api/v1/opportunities/{opportunity_id}
```

Returns information about a specific opportunity.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 1,
  "title": "IT Support Services",
  "description": "Providing IT support services for government agency",
  "agency": "Department of Defense",
  "solicitation_number": "DOD-2025-IT-001",
  "naics_code": "541512",
  "posted_date": "2025-03-15T00:00:00",
  "due_date": "2025-04-15T00:00:00",
  "url": "https://sam.gov/opportunity/123456",
  "status": "active",
  "estimated_value": 500000,
  "created_at": "2025-03-24T00:00:00"
}
```

### Update Opportunity

```
PUT /api/v1/opportunities/{opportunity_id}
```

Updates an opportunity's information.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title": "Updated IT Support Services",
  "due_date": "2025-04-20T00:00:00"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated IT Support Services",
  "description": "Providing IT support services for government agency",
  "agency": "Department of Defense",
  "solicitation_number": "DOD-2025-IT-001",
  "naics_code": "541512",
  "posted_date": "2025-03-15T00:00:00",
  "due_date": "2025-04-20T00:00:00",
  "url": "https://sam.gov/opportunity/123456",
  "status": "active",
  "estimated_value": 500000,
  "created_at": "2025-03-24T00:00:00"
}
```

## Proposals

### Create Proposal

```
POST /api/v1/proposals/
```

Creates a new proposal.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title": "DOD IT Support Proposal",
  "opportunity_id": 1,
  "company_id": 1,
  "status": "draft",
  "submission_date": "2025-04-10T00:00:00"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "DOD IT Support Proposal",
  "opportunity_id": 1,
  "company_id": 1,
  "created_by_id": 1,
  "status": "draft",
  "submission_date": "2025-04-10T00:00:00",
  "created_at": "2025-03-24T00:00:00"
}
```

### Get Proposals

```
GET /api/v1/proposals/
```

Returns a list of proposals.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `status` (optional): Filter by status (draft, in_progress, review, submitted, won, lost)
- `company_id` (optional): Filter by company ID

**Response:**
```json
[
  {
    "id": 1,
    "title": "DOD IT Support Proposal",
    "opportunity_id": 1,
    "company_id": 1,
    "created_by_id": 1,
    "status": "draft",
    "submission_date": "2025-04-10T00:00:00",
    "created_at": "2025-03-24T00:00:00"
  }
]
```

### Get Proposal by ID

```
GET /api/v1/proposals/{proposal_id}
```

Returns information about a specific proposal.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 1,
  "title": "DOD IT Support Proposal",
  "opportunity_id": 1,
  "company_id": 1,
  "created_by_id": 1,
  "status": "draft",
  "submission_date": "2025-04-10T00:00:00",
  "created_at": "2025-03-24T00:00:00"
}
```

### Update Proposal

```
PUT /api/v1/proposals/{proposal_id}
```

Updates a proposal's information.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title": "Updated DOD IT Support Proposal",
  "status": "in_progress"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated DOD IT Support Proposal",
  "opportunity_id": 1,
  "company_id": 1,
  "created_by_id": 1,
  "status": "in_progress",
  "submission_date": "2025-04-10T00:00:00",
  "created_at": "2025-03-24T00:00:00"
}
```

## Error Responses

All API endpoints return standard HTTP status codes:

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

Error responses include a detail message:

```json
{
  "detail": "Error message describing the issue"
}
```

## Rate Limiting

API requests are limited to 100 requests per minute per user. If you exceed this limit, you'll receive a `429 Too Many Requests` response.

## Pagination

List endpoints support pagination using the following query parameters:

- `skip`: Number of items to skip (default: 0)
- `limit`: Maximum number of items to return (default: 100, max: 1000)

Example:
```
GET /api/v1/opportunities/?skip=20&limit=10
```

This would return items 21-30 in the collection.
