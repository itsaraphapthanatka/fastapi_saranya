from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class About(Base):
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, nullable=False)
    desc = Column("desc", Text)
    founderName = Column("founderName", String(255), nullable=True)
    founderDesc = Column("founderDesc", Text, nullable=True)
    founderImg = Column("founderImg", String(255), nullable=True)
    sec2Desc = Column("sec2Desc", Text, nullable=True)
    sec2Img = Column("sec2Img", String(255), nullable=True)
    sec3Desc = Column("sec3Desc", Text, nullable=True)
    sec3img = Column("sec3img", String(255), nullable=True)
    sec3Experience = Column("sec3Experience", String(10), nullable=True)
    sec4Desc = Column("sec4Desc", Text, nullable=True)
    sec4img = Column("sec4img", String(255), nullable=True)

    def __repr__(self):
        return f"<About(id={self.id!r}, founderName={self.founderName!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "desc": self.desc,
            "founderName": self.founderName,
            "founderDesc": self.founderDesc,
            "founderImg": self.founderImg,
            "sec2Desc": self.sec2Desc,
            "sec2Img": self.sec2Img,
            "sec3Desc": self.sec3Desc,
            "sec3img": self.sec3img,
            "sec3Experience": self.sec3Experience,
            "sec4Desc": self.sec4Desc,
            "sec4img": self.sec4img,
        }