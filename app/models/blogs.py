from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Blogs(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    img = Column(String(255), nullable=True)
    blogsType = Column(String(100), nullable=True)
    createBy = Column(String(100), nullable=True)
    createDate = Column(String(100), nullable=True)
    editBy = Column(String(100), nullable=True)
    editDate = Column(String(100), nullable=True)
    delBy = Column(String(100), nullable=True)
    delDate = Column(String(100), nullable=True)
    blogsStatus = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<Blogs(id={self.id!r}, title={self.title!r}, content={self.content!r}, img={self.img!r}, blogsType={self.blogsType!r}, createBy={self.createBy!r}, createDate={self.createDate!r}, editBy={self.editBy!r}, editDate={self.editDate!r}, delBy={self.delBy!r}, delDate={self.delDate!r}, blogsStatus={self.blogsStatus!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "img": self.img,
            "blogsType": self.blogsType,
            "createBy": self.createBy,
            "createDate": self.createDate,
            "editBy": self.editBy,
            "editDate": self.editDate,
            "delBy": self.delBy,
            "delDate": self.delDate,
            "blogsStatus": self.blogsStatus,
        }