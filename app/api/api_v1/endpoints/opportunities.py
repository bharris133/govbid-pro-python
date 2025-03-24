from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.db.base import get_db
from app.models.models import Opportunity
from app.schemas.schemas import Opportunity as OpportunitySchema, OpportunityCreate, OpportunityUpdate

router = APIRouter()


@router.get("/", response_model=List[OpportunitySchema])
def read_opportunities(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve opportunities.
    """
    opportunities = db.query(Opportunity).offset(skip).limit(limit).all()
    return opportunities


@router.post("/", response_model=OpportunitySchema)
def create_opportunity(
    *,
    db: Session = Depends(get_db),
    opportunity_in: OpportunityCreate,
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """
    Create new opportunity.
    """
    opportunity = Opportunity(
        title=opportunity_in.title,
        description=opportunity_in.description,
        agency=opportunity_in.agency,
        solicitation_number=opportunity_in.solicitation_number,
        naics_code=opportunity_in.naics_code,
        due_date=opportunity_in.due_date,
        posted_date=opportunity_in.posted_date,
        status=opportunity_in.status,
        url=opportunity_in.url,
        estimated_value=opportunity_in.estimated_value,
        source=opportunity_in.source,
        fit_score=opportunity_in.fit_score,
        win_probability=opportunity_in.win_probability,
    )
    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    return opportunity


@router.get("/{opportunity_id}", response_model=OpportunitySchema)
def read_opportunity(
    *,
    db: Session = Depends(get_db),
    opportunity_id: int,
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """
    Get opportunity by ID.
    """
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opportunity


@router.put("/{opportunity_id}", response_model=OpportunitySchema)
def update_opportunity(
    *,
    db: Session = Depends(get_db),
    opportunity_id: int,
    opportunity_in: OpportunityUpdate,
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """
    Update an opportunity.
    """
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    
    update_data = opportunity_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(opportunity, field, value)
    
    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    return opportunity


@router.delete("/{opportunity_id}", response_model=OpportunitySchema)
def delete_opportunity(
    *,
    db: Session = Depends(get_db),
    opportunity_id: int,
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """
    Delete an opportunity.
    """
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    
    db.delete(opportunity)
    db.commit()
    return opportunity
