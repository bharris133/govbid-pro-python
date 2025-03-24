from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.db.base import get_db
# For proposals.py
from app.models.models import Proposal, User, Company, Opportunity
from app.schemas.schemas import ProposalCreate, ProposalUpdate, Proposal as ProposalSchema

router = APIRouter()


@router.get("/", response_model=List[ProposalSchema])
def read_proposals(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve proposals.
    """
    # If user is not a superuser, only return proposals for their company
    if not current_user.is_superuser:
        proposals = db.query(Proposal).filter(
            Proposal.company_id == current_user.company_id
        ).offset(skip).limit(limit).all()
    else:
        proposals = db.query(Proposal).offset(skip).limit(limit).all()
    return proposals


@router.post("/", response_model=ProposalSchema)
def create_proposal(
    *,
    db: Session = Depends(get_db),
    proposal_in: ProposalCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new proposal.
    """
    proposal = Proposal(
        title=proposal_in.title,
        opportunity_id=proposal_in.opportunity_id,
        company_id=proposal_in.company_id,
        created_by_id=current_user.id,
        status=proposal_in.status,
        submission_date=proposal_in.submission_date,
    )
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return proposal


@router.get("/{proposal_id}", response_model=ProposalSchema)
def read_proposal(
    *,
    db: Session = Depends(get_db),
    proposal_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get proposal by ID.
    """
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    # Check if user has access to this proposal
    if not current_user.is_superuser and proposal.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return proposal


# app/api/api_v1/endpoints/proposals.py
# Find the update_proposal function and make similar changes

@router.put("/{proposal_id}", response_model=ProposalSchema)
def update_proposal(
    *,
    db: Session = Depends(get_db),
    proposal_id: int,
    proposal_in: ProposalUpdate,
    current_user: User = Depends(get_current_active_user),
):
    """
    Update a proposal.
    """
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    # Update only the fields that are provided
    update_data = proposal_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(proposal, field, value)
    
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return proposal



@router.delete("/{proposal_id}", response_model=ProposalSchema)
def delete_proposal(
    *,
    db: Session = Depends(get_db),
    proposal_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a proposal.
    """
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    # Check if user has access to this proposal
    if not current_user.is_superuser and proposal.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(proposal)
    db.commit()
    return proposal
