from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class OEM(Base):
    __tablename__ = "oem"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    position = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<OEM(id={self.id!r}, name={self.name!r}, position={self.position!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "position": self.position,
        }
