from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uname = Column(String(255), nullable=False)
    upass = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    ustatus = Column(String[10], nullable=False, default="active")
    createuser = Column(String(255), nullable=True)
    createdate = Column(String(255), nullable=True)
    edituser = Column(String(255), nullable=True)
    editdate = Column(String(255), nullable=True)
    deluser = Column(String(255), nullable=True)
    deldate = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Users(id={self.id!r}, uname={self.uname!r}, upass={self.upass!r}, email={self.email!r}, ustatus={self.ustatus!r}, createuser={self.createuser!r}, createdate={self.createdate!r}, edituser={self.edituser!r}, editdate={self.editdate!r}, deluser={self.deluser!r}, deldate={self.deldate!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "uname": self.uname,
            "upass": self.upass,
            "email": self.email,
            "ustatus": self.ustatus,
            "createuser": self.createuser,
            "createdate": self.createdate,
            "edituser": self.edituser,
            "editdate": self.editdate,
            "deluser": self.deluser,
            "deldate": self.deldate,
        }