from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class ODM(Base):
    __tablename__ = "odm"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    name_th = Column(String(255), nullable=True)
    position = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<ODM(id={self.id!r}, name={self.name!r}, name_th={self.name_th!r}, position={self.position!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_th": self.name_th,
            "position": self.position,
        }