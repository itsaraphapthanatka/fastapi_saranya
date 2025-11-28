from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class About(Base):
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, nullable=False)
    desc = Column("desc", Text)
    desc_th = Column("desc_th", Text)
    founderName = Column("founderName", String(255), nullable=True)
    founderName_th = Column("founderName_th", String(255), nullable=True)
    founderDesc = Column("founderDesc", Text, nullable=True)
    founderDesc_th = Column("founderDesc_th", Text, nullable=True)
    founderImg = Column("founderImg", String(255), nullable=True)
    sec2Desc = Column("sec2Desc", Text, nullable=True)
    sec2Desc_th = Column("sec2Desc_th", Text, nullable=True)
    sec2Img = Column("sec2Img", String(255), nullable=True)
    sec3Desc = Column("sec3Desc", Text, nullable=True)
    sec3Desc_th = Column("sec3Desc_th", Text, nullable=True)
    sec3img = Column("sec3img", String(255), nullable=True)
    sec3Experience = Column("sec3Experience", String(10), nullable=True)
    sec4Desc = Column("sec4Desc", Text, nullable=True)
    sec4Desc_th = Column("sec4Desc_th", Text, nullable=True)
    sec4img = Column("sec4img", String(255), nullable=True)

    def __repr__(self):
        return f"<About(id={self.id!r}, founderName={self.founderName!r}, founderName_th={self.founderName_th!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "desc": self.desc,
            "desc_th": self.desc_th,
            "founderName": self.founderName,
            "founderName_th": self.founderName_th,
            "founderDesc": self.founderDesc,
            "founderDesc_th": self.founderDesc_th,
            "founderImg": self.founderImg,
            "sec2Desc": self.sec2Desc,
            "sec2Desc_th": self.sec2Desc_th,
            "sec2Img": self.sec2Img,
            "sec3Desc": self.sec3Desc,
            "sec3Desc_th": self.sec3Desc_th,
            "sec3img": self.sec3img,
            "sec3Experience": self.sec3Experience,
            "sec4Desc": self.sec4Desc,
            "sec4Desc_th": self.sec4Desc_th,
            "sec4img": self.sec4img,
        }