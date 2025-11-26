from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Standardset(Base):
    __tablename__ = "standard_set"

    id = Column(Integer, primary_key=True, index=True)
    standid =  Column(Integer, nullable=False)
    standsetname = Column(String(255), nullable=False)
    standsetdesc = Column(Text, nullable=True)
    standsetimg = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Standardset(id={self.id!r}, standid={self.standid!r}, standsetname={self.standsetname!r}, standsetimg={self.standsetimg!r}, standsetdesc={self.standsetdesc!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "standid": self.standid,
            "standsetname": self.standsetname,
            "standsetdesc": self.standsetdesc,
            "standsetimg": self.standsetimg,
        }