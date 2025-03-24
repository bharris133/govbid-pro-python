from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    company_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

# Company schemas
class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    naics_codes: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass

class CompanyInDBBase(CompanyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class Company(CompanyInDBBase):
    pass

# Opportunity schemas
class OpportunityBase(BaseModel):
    title: str
    description: Optional[str] = None
    agency: Optional[str] = None
    solicitation_number: Optional[str] = None
    naics_code: Optional[str] = None
    posted_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    url: Optional[str] = None
    status: str
    estimated_value: Optional[float] = None

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    agency: Optional[str] = None
    solicitation_number: Optional[str] = None
    naics_code: Optional[str] = None
    posted_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    url: Optional[str] = None
    status: Optional[str] = None
    estimated_value: Optional[float] = None

class OpportunityInDBBase(OpportunityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class Opportunity(OpportunityInDBBase):
    pass

# Proposal schemas
class ProposalBase(BaseModel):
    title: str
    opportunity_id: Optional[int] = None
    company_id: int
    status: str
    submission_date: Optional[datetime] = None

class ProposalCreate(ProposalBase):
    pass

class ProposalUpdate(BaseModel):
    title: Optional[str] = None
    opportunity_id: Optional[int] = None
    company_id: Optional[int] = None
    status: Optional[str] = None
    submission_date: Optional[datetime] = None

class ProposalInDBBase(ProposalBase):
    id: int
    created_by_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class Proposal(ProposalInDBBase):
    pass

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None

# Generic message schema
class Message(BaseModel):
    message: str
