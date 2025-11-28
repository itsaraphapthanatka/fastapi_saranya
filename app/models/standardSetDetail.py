from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class StandardSetDetail(Base):
    __tablename__ = "standard_set_detail"

    id = Column(Integer, primary_key=True, index=True)
    s_id = Column(Integer, nullable=False)
    s_set_id = Column(Integer, nullable=False)
    s_set_title = Column(String(255), nullable=False)
    s_set_title_th = Column(String(255), nullable=True)
    s_set_desc = Column(Text, nullable=True)
    s_set_desc_th = Column(Text, nullable=True)
    s_set_img = Column(String(255), nullable=False)
    s_set_chk_main = Column(Integer, nullable=False)
    position = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<StandardSetDetail(id={self.id!r}, s_id={self.s_id!r}, s_set_id={self.s_set_id!r}, s_set_title={self.s_set_title!r}, s_set_title_th={self.s_set_title_th!r}, s_set_desc={self.s_set_desc!r}, s_set_desc_th={self.s_set_desc_th!r}, s_set_img={self.s_set_img!r}, s_set_chk_main={self.s_set_chk_main!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "s_id": self.s_id,
            "s_set_id": self.s_set_id,
            "s_set_title": self.s_set_title,
            "s_set_title_th": self.s_set_title_th,
            "s_set_desc": self.s_set_desc,
            "s_set_desc_th": self.s_set_desc_th,
            "s_set_img": self.s_set_img,
            "s_set_chk_main": self.s_set_chk_main,
            "position": self.position,
        }