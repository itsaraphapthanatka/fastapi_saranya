from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    factoryAddress = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    workinghour = Column(Text, nullable=False)
    facebook = Column(String(255), nullable=True)
    instagram = Column(String(255), nullable=True)
    linkedin = Column(String(255), nullable=True)
    x_twitter = Column(String(255), nullable=True)
    line = Column(String(255), nullable=True)
    tiktok = Column(String(255), nullable=True)
    googlemap = Column(Text, nullable=True)
    youtube = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Contact(id={self.id!r}, name={self.name!r}, factoryAddress={self.factoryAddress!r}, phone={self.phone!r}, email={self.email!r}, workinghour={self.workinghour!r}, facebook={self.facebook!r}, instagram={self.instagram!r}, linkedin={self.linkedin!r}, x_twitter={self.x_twitter!r}, line={self.line!r}, tiktok={self.tiktok!r}, googlemap={self.googlemap!r}, youtube={self.youtube!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "factoryAddress": self.factoryAddress,
            "phone": self.phone,
            "email": self.email,
            "workinghour": self.workinghour,
            "facebook": self.facebook,
            "instagram": self.instagram,
            "linkedin": self.linkedin,
            "x_twitter": self.x_twitter,
            "line": self.line,
            "tiktok": self.tiktok,
            "googlemap": self.googlemap,
            "youtube": self.youtube,
        }