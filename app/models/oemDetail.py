from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class OEMDtail(Base):
    __tablename__ = "oem_detail"

    id = Column(Integer, primary_key=True, index=True)
    oem_id = Column(Integer, nullable=False)
    img = Column(String(255), nullable=False)
    position = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<OEMDetail(id={self.id!r}, oem_id={self.odm_id!r}, img={self.img!r}, position={self.position!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "oem_id": self.odm_id,
            "img": self.img,
            "position": self.position,
        }