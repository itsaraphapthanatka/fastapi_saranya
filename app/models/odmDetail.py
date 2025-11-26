from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class OdmDetail(Base):
    __tablename__ = "odm_detail"

    id = Column(Integer, primary_key=True, index=True)
    odm_id = Column(Integer, nullable=False)
    img = Column(String(255), nullable=False)
    position = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<OdmDetail(id={self.id!r}, odm_id={self.odm_id!r}, img={self.img!r}, position={self.position!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "odm_id": self.odm_id,
            "img": self.img,
            "position": self.position,
        }