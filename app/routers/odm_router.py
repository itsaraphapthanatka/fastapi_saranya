from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.odm import ODM
from datetime import datetime
import os
import shutil
from pydantic import BaseModel

router = APIRouter(
    prefix="/odm",
    tags=["odm"]
)

class ODMCreate(BaseModel):
    name: str
    name_th: str

class ODMUpdate(BaseModel):
    name: str = None
    name_th: str = None

class ODMResponse(BaseModel):
    id: int
    name: str
    name_th: str
    position: int

    class Config:
        orm_mode = True

@router.get("/")
def get_odms(db: Session = Depends(get_db)):
    odms = db.query(ODM).all()
    return odms

@router.post("/", response_model=ODMResponse)
def create_odm(payload: ODMCreate, db: Session = Depends(get_db)):
    max_position = db.query(func.max(ODM.id)).scalar() or 0
    odm = ODM(name=payload.name, name_th=payload.name_th, position=max_position + 1)
    db.add(odm)
    db.commit()
    db.refresh(odm)
    return odm

@router.put("/reorder")
def reorder_odms(payload: dict, db: Session = Depends(get_db)):
    order = payload.get("orderIds", [])
    print("Reordering OEMs with order:", order)

    for index, odm_id in enumerate(order):
        odm = db.query(ODM).filter(ODM.id == odm_id).first()
        if odm:
            odm.position = index

    db.commit()
    return {"detail": "ok"}

@router.get("/{odm_id}")
def get_odm(odm_id: int, db: Session = Depends(get_db)):
    odm = db.query(ODM).filter(ODM.id == odm_id).first()
    if not odm:
        raise HTTPException(status_code=404, detail="ODM not found")
    return odm

@router.put("/{odm_id}")
def update_odm(odm_id: int, payload: ODMUpdate, db: Session = Depends(get_db)):
    odm = db.query(ODM).filter(ODM.id == odm_id).first()
    if not odm:
        raise HTTPException(status_code=404, detail="ODM not found")
    
    if payload.name:
        odm.name = payload.name
    if payload.name_th:
        odm.name_th = payload.name_th   
    
    db.commit()
    db.refresh(odm)
    return odm

@router.delete("/{odm_id}")
def delete_odm(odm_id: int, db: Session = Depends(get_db)):
    odm = db.query(ODM).filter(ODM.id == odm_id).first()
    if not odm:
        raise HTTPException(status_code=404, detail="ODM not found")
    
    db.delete(odm)
    db.commit()
    return {"detail": "ODM deleted successfully"}