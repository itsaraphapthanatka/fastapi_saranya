from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class CollectionImage(Base):
    __tablename__ = "collection_image"

    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, nullable=False)
    collection_img = Column(String(255), nullable=False)
    position = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<CollectionImage(id={self.id!r}, collection_id={self.collection_id}, collection_img={self.collection_img!r}, position={self.position!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "collection_id": self.collection_id,
            "collection_img": self.collection_img,
            "position": self.position,
        }