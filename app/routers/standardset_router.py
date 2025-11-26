from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.standardSet import Standardset
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(
    prefix="/standardset",
    tags=["standardset"]
)

class StandardSetCreate(BaseModel):
    standid: int
    standsetname: str
    standsetdesc: str


@router.get("/")
def get_standardsets(db: Session = Depends(get_db)):
    standardsets = db.query(Standardset).all()
    return standardsets

@router.post("/")
def create_standardset(payload: StandardSetCreate, db: Session = Depends(get_db)):
    print("Creating Standardset with payload:", payload)
    standardset = Standardset(standid=payload.standid, standsetname=payload.standsetname, standsetdesc=payload.standsetdesc)
    db.add(standardset)
    db.commit()
    db.refresh(standardset)
    return standardset

@router.get("/{standardset_id}")
def get_standardset(standardset_id: int, db: Session = Depends(get_db)):
    standardset = db.query(Standardset).filter(Standardset.id == standardset_id).first()
    if not standardset:
        raise HTTPException(status_code=404, detail="Standardset not found")
    return standardset

@router.get("/standard/{standard_id}")
def get_standardsets_by_standid(standard_id: int, db: Session = Depends(get_db)):
    standardsets = db.query(Standardset).filter(Standardset.standid == standard_id).all()
    if not standardsets:
        raise HTTPException(status_code=404, detail="No Standardsets found for the given standard ID")
    return standardsets

@router.put("/{standardset_id}")
def update_standardset(standardset_id: int, name: str = None, standid: int = None, standsetname: str = None, standsetimg: str = None, db: Session = Depends(get_db)):
    standardset = db.query(Standardset).filter(Standardset.id == standardset_id).first()
    if not standardset:
        raise HTTPException(status_code=404, detail="Standardset not found")
    
    if name:
        standardset.name = name
    if standid:
        standardset.standid = standid
    if standsetname:
        standardset.standsetname = standsetname
    if standsetimg:
        standardset.standsetimg = standsetimg
    
    db.commit()
    db.refresh(standardset)
    return standardset

@router.delete("/{standardset_id}")
def delete_standardset(standardset_id: int, db: Session = Depends(get_db)):
    standardset = db.query(Standardset).filter(Standardset.id == standardset_id).first()
    if not standardset:
        raise HTTPException(status_code=404, detail="Standardset not found")
    
    db.delete(standardset)
    db.commit()
    return {"detail": "Standardset deleted successfully"}