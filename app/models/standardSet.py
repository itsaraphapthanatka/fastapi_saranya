from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Standardset(Base):
    __tablename__ = "standard_set"

    id = Column(Integer, primary_key=True, index=True)
    standid =  Column(Integer, nullable=False)
    standsetname = Column(String(255), nullable=False)
    standsetname_th = Column(String(255), nullable=True)
    standsetdesc = Column(Text, nullable=True)
    standsetdesc_th = Column(Text, nullable=True)
    standsetimg = Column(Text, nullable=True)
    position = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Standardset(id={self.id!r}, standid={self.standid!r}, standsetname={self.standsetname!r}, standsetname_th={self.standsetname_th!r}, standsetimg={self.standsetimg!r}, standsetdesc={self.standsetdesc!r}, position={self.position!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "standid": self.standid,
            "standsetname": self.standsetname,
            "standsetname_th": self.standsetname_th,
            "standsetdesc": self.standsetdesc,
            "standsetdesc_th": self.standsetdesc_th,
            "standsetimg": self.standsetimg,
            "position": self.position,
        }