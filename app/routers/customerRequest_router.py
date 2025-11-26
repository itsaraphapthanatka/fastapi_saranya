from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.customerRequest import CustomerRequest
from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/customer_request",
    tags=["customer_request"]
)

@router.get("/")
def get_customer_requests(db: Session = Depends(get_db)):
    customer_requests = db.query(CustomerRequest).all()
    return customer_requests

class CustomerRequestCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    product_type: Optional[str] = None
    qty_size: Optional[str] = None
    addition_details: Optional[str] = None
    createdate: Optional[datetime] = None

@router.post("/")
def create_customer_request(
    request: CustomerRequestCreate,
    db: Session = Depends(get_db)
    ):
    customer_request = CustomerRequest(
        name=request.name,
        email=request.email,
        phone=request.phone,
        product_type=request.product_type,
        qty_size=request.qty_size,
        addition_details=request.addition_details,
        createdate=request.createdate or datetime.now(timezone.utc)
    )
    db.add(customer_request)
    db.commit()
    db.refresh(customer_request)
    return customer_request

@router.get("/{customer_request_id}")
def get_customer_request(customer_request_id: int, db: Session = Depends(get_db)):
    customer_request = db.query(CustomerRequest).filter(CustomerRequest.id == customer_request_id).first()
    if not customer_request:
        raise HTTPException(status_code=404, detail="Customer Request not found")
    return customer_request

@router.put("/{customer_request_id}")
def update_customer_request(
    customer_request_id: int,
    request: CustomerRequestCreate,
    db: Session = Depends(get_db)
    ):
    customer_request = db.query(CustomerRequest).filter(CustomerRequest.id == customer_request_id).first()
    if not customer_request:
        raise HTTPException(status_code=404, detail="Customer Request not found")
    
    customer_request.name = request.name
    customer_request.email = request.email
    customer_request.phone = request.phone
    customer_request.product_type = request.product_type
    customer_request.qty_size = request.qty_size
    customer_request.addition_details = request.addition_details
    customer_request.createdate = request.createdate or customer_request.createdate
    
    db.commit()
    db.refresh(customer_request)
    return customer_request

@router.delete("/{customer_request_id}")
def delete_customer_request(customer_request_id: int, db: Session = Depends(get_db)):
    customer_request = db.query(CustomerRequest).filter(CustomerRequest.id == customer_request_id).first()
    if not customer_request:
        raise HTTPException(status_code=404, detail="Customer Request not found")
    
    db.delete(customer_request)
    db.commit()
    return {"detail": "Customer Request deleted successfully"}
