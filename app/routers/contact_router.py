from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.contact import Contact
from typing import Optional

router = APIRouter(
    prefix="/contact",
    tags=["contact"]
)

class ContactUpdate(BaseModel):
    factoryAddress: Optional[str] = None
    factoryAddress_th: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    workinghour: Optional[str] = None
    workinghour_th: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    x_twitter: Optional[str] = None
    linkedin: Optional[str] = None
    line: Optional[str] = None
    tiktok: Optional[str] = None
    wechat: Optional[str] = None
    googlemap: Optional[str] = None
    youtube: Optional[str] = None

@router.get("/")
def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    return contacts

@router.post("/")
def create_contact(
        factoryAddress: str,
        factoryAddress_th: str,
        phone: str,
        email: str,
        workingHours: str,
        workingHours_th: str,
        facebook: str,
        instagram: str,
        x_twitter: str,
        linkedin: str,
        line: str,
        tiktok: str,
        wechat: str,
        googlemap: str,
        youtube: str,
        db: Session = Depends(get_db)
    ):
    contact = Contact(
        factoryAddress=factoryAddress,
        factoryAddress_th=factoryAddress_th,
        phone=phone,
        email=email,
        workingHours=workingHours,
        workingHours_th=workingHours_th,
        facebook=facebook,
        instagram=instagram,
        x_twitter=x_twitter,
        linkedin=linkedin,
        line=line,
        tiktok=tiktok,
        wechat=wechat,
        googlemap=googlemap,
        youtube=youtube
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

@router.get("/{contact_id}")
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}")
def update_contact(
        contact_id: int,
        contact_update: ContactUpdate,
        db: Session = Depends(get_db)
    ):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    for field, value in contact_update.dict(exclude_unset=True).items():
        setattr(contact, field, value)

    db.commit()
    db.refresh(contact)
    return contact

@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db.delete(contact)
    db.commit()
    return {"detail": "Contact deleted successfully"}
