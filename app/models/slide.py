from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Slide(Base):
    __tablename__ = "slide"

    id = Column(Integer, primary_key=True, index=True)
    slide_image = Column(String(255), nullable=False)
    slide_desc = Column(Text, nullable=True)
    position = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Slide(id={self.id!r}, slide_image={self.slide_image!r}, slide_desc={self.slide_desc!r}, position={self.position!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "slide_image": self.slide_image,
            "slide_desc": self.slide_desc,
            "position": self.position,
        }