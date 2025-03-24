from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, Float, Table, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    website = Column(String, nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    naics_codes = Column(String, nullable=True)  # Comma-separated list of NAICS codes

    # Relationships
    users = relationship("User", back_populates="company")
    proposals = relationship("Proposal", back_populates="company")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="users")
    created_proposals = relationship("Proposal", back_populates="created_by", foreign_keys="Proposal.created_by_id")
    team_memberships = relationship("ProposalTeamMember", back_populates="user")
    roles = relationship("UserRole", back_populates="user")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    permissions = Column(JSON, nullable=True)  # JSON field for storing permissions

    # Relationships
    users = relationship("UserRole", back_populates="role")


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    agency = Column(String, nullable=True, index=True)
    solicitation_number = Column(String, nullable=True, index=True)
    naics_code = Column(String, nullable=True, index=True)
    posted_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    url = Column(String, nullable=True)
    status = Column(String, index=True)  # active, archived, etc.
    estimated_value = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    # Relationships
    proposals = relationship("Proposal", back_populates="opportunity")
    documents = relationship("OpportunityDocument", back_populates="opportunity")


class OpportunityDocument(Base):
    __tablename__ = "opportunity_documents"

    id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"))
    title = Column(String)
    file_url = Column(String)
    file_type = Column(String, nullable=True)  # pdf, doc, etc.
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    opportunity = relationship("Opportunity", back_populates="documents")


class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, index=True)  # draft, in_progress, review, submitted, won, lost
    submission_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    # Relationships
    opportunity = relationship("Opportunity", back_populates="proposals")
    company = relationship("Company", back_populates="proposals")
    created_by = relationship("User", back_populates="created_proposals", foreign_keys=[created_by_id])
    sections = relationship("ProposalSection", back_populates="proposal")
    team_members = relationship("ProposalTeamMember", back_populates="proposal")
    subcontractors = relationship("ProposalSubcontractor", back_populates="proposal")


class ProposalSection(Base):
    __tablename__ = "proposal_sections"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("proposals.id"))
    title = Column(String)
    content = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    template_id = Column(Integer, ForeignKey("section_templates.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    # Relationships
    proposal = relationship("Proposal", back_populates="sections")
    template = relationship("SectionTemplate", back_populates="sections")


class SectionTemplate(Base):
    __tablename__ = "section_templates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text, nullable=True)
    category = Column(String, nullable=True)  # technical, management, past performance, etc.
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    # Relationships
    sections = relationship("ProposalSection", back_populates="template")


class ProposalTeamMember(Base):
    __tablename__ = "proposal_team_members"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("proposals.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String, nullable=True)  # writer, reviewer, approver, etc.
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    proposal = relationship("Proposal", back_populates="team_members")
    user = relationship("User", back_populates="team_memberships")


class Subcontractor(Base):
    __tablename__ = "subcontractors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    website = Column(String, nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    naics_codes = Column(String, nullable=True)  # Comma-separated list of NAICS codes
    capabilities = Column(Text, nullable=True)
    past_performance = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    # Relationships
    proposals = relationship("ProposalSubcontractor", back_populates="subcontractor")


class ProposalSubcontractor(Base):
    __tablename__ = "proposal_subcontractors"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("proposals.id"))
    subcontractor_id = Column(Integer, ForeignKey("subcontractors.id"))
    role = Column(String, nullable=True)
    work_description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    proposal = relationship("Proposal", back_populates="subcontractors")
    subcontractor = relationship("Subcontractor", back_populates="proposals")


class PricingData(Base):
    __tablename__ = "pricing_data"

    id = Column(Integer, primary_key=True, index=True)
    contract_number = Column(String, index=True, nullable=True)
    agency = Column(String, index=True, nullable=True)
    product_service = Column(String, index=True)
    description = Column(Text, nullable=True)
    unit_price = Column(Float)
    quantity = Column(Integer, nullable=True)
    unit_of_measure = Column(String, nullable=True)
    award_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User")
