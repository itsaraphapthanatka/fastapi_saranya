from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class NaturalFibers(Base):
    __tablename__ = "natural_fibers"

    id = Column(Integer, primary_key=True, index=True)
    img = Column(String(255), nullable=False)
    position = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<NaturalFibers(id={self.id!r}, img={self.img!r}, position={self.position!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "img": self.img,
            "position": self.position,
        }   