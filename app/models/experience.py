from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True, index=True)
    img = Column(String(255), nullable=False)
    position = Column(Integer, nullable=False, default=0)
    
    def __repr__(self):
        return f"<Experience(id={self.id!r}, img={self.img!r}, position={self.position!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "img": self.img,
            "position": self.position,
        }