from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class CustomerRequest(Base):
    __tablename__ = "customer_request"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    product_type = Column(String(255), nullable=True)
    qty_size = Column(String(100), nullable=True)
    addition_details = Column(Text, nullable=True)
    createdate = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<CustomerRequest(id={self.id!r}, name={self.name!r}, email={self.email!r}, phone={self.phone!r}, product_type={self.product_type!r}, qty_size={self.qty_size!r}, addition_details={self.addition_details!r}, createdate={self.createdate!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "product_type": self.product_type,
            "qty_size": self.qty_size,
            "addition_details": self.addition_details,
            "createdate": self.createdate,
        }