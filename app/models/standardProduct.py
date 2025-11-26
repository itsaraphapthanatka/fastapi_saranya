from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class StandardProduct(Base):
    __tablename__ = "standard_product"

    id = Column(Integer, primary_key=True, index=True)
    standname = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<StandardProduct(id={self.id!r}, standname={self.standname!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "standname": self.standname,
        }