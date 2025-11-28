from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Collection(Base):
    __tablename__ = "collection"

    id = Column(Integer, primary_key=True, index=True)
    collec_name = Column(String(255), nullable=False)
    collec_name_th = Column(String(255), nullable=True) 
    

    def __repr__(self):
        return f"<Collection(id={self.id!r}, collec_name={self.collec_name!r}, collec_name_th={self.collec_name_th!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "collec_name": self.collec_name,
            "collec_name_th": self.collec_name_th,  
        }