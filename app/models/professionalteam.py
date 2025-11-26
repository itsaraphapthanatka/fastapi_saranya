from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class ProfessionalTeam(Base):
    __tablename__ = "professional_team"

    id = Column(Integer, primary_key=True, index=True)
    img = Column(String(255), nullable=False)
    position = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<ProfessionalTeam(id={self.id!r}, img={self.img!r}, position={self.position!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "img": self.img,
            "position": self.position,
        }