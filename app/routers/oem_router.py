from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.oem import OEM
from datetime import datetime
import os
import shutil
from pydantic import BaseModel

router = APIRouter(
    prefix="/oem",
    tags=["oem"]
)

class OEMCreate(BaseModel):
    name: str

class OEMUpdate(BaseModel):
    name: str = None

class OEMResponse(BaseModel):
    id: int
    name: str
    position: int

    class Config:
        orm_mode = True


@router.get("/")
def get_oems(db: Session = Depends(get_db)):
    oems = db.query(OEM).order_by(OEM.position.asc()).all()
    return oems

@router.post("/", response_model=OEMResponse)
def create_oem(payload: OEMCreate, db: Session = Depends(get_db)):
    print("Creating OEM with name:", payload)
    max_position = db.query(func.max(OEM.id)).scalar() or 0
    oem = OEM(name=payload.name, position=max_position + 1)
    db.add(oem)
    db.commit()
    db.refresh(oem)
    return oem


@router.get("/{oem_id}")
def get_oem(oem_id: int, db: Session = Depends(get_db)):
    oem = db.query(OEM).filter(OEM.id == oem_id).first()
    if not oem:
        raise HTTPException(status_code=404, detail="OEM not found")
    return oem

@router.put("/reorder")
def reorder_oems(payload: dict, db: Session = Depends(get_db)):
    order = payload.get("orderIds", [])
    print("Reordering OEMs with order:", order)

    for index, oem_id in enumerate(order):
        oem = db.query(OEM).filter(OEM.id == oem_id).first()
        if oem:
            oem.position = index

    db.commit()
    return {"detail": "ok"}

@router.put("/{oem_id}")
def update_oem(oem_id: int, name: str = None, db: Session = Depends(get_db)):
    oem = db.query(OEM).filter(OEM.id == oem_id).first()
    if not oem:
        raise HTTPException(status_code=404, detail="OEM not found")
    
    if name:
        oem.name = name
    
    db.commit()
    db.refresh(oem)
    return oem

@router.delete("/{oem_id}")
def delete_oem(oem_id: int, db: Session = Depends(get_db)):
    oem = db.query(OEM).filter(OEM.id == oem_id).first()
    if not oem:
        raise HTTPException(status_code=404, detail="OEM not found")
    
    db.delete(oem)
    db.commit()
    return {"detail": "OEM deleted successfully"}

