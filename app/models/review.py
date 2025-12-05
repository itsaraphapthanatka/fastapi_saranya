from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base

class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    title_th = Column(String(255), nullable=True)
    desc = Column(Text, nullable=False)
    desc_th = Column(Text, nullable=True)
    src = Column(String(255), nullable=False)
    reviewstatus = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)  
    createBy = Column(String(255), nullable=False)
    createAt = Column(DateTime, nullable=False)
    editBy = Column(String(255), nullable=False)
    editAt = Column(DateTime, nullable=False)
    delBy = Column(String(255), nullable=False)
    delAt = Column(DateTime, nullable=False)
    
    

    def __repr__(self):
        return f"<Review(id={self.id!r}, title={self.title!r}, title_th={self.title_th!r}, desc={self.desc!r}, desc_th={self.desc_th!r}, src={self.src!r}, reviewstatus={self.reviewstatus!r}, position={self.position!r}, createBy={self.createBy!r}, createAt={self.createAt!r}, editBy={self.editBy!r}, editAt={self.editAt!r}, delBy={self.delBy!r}, delAt={self.delAt!r})>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "title_th": self.title_th,
            "desc": self.desc,
            "desc_th": self.desc_th,
            "src": self.src,    
            "reviewstatus": self.reviewstatus,
            "position": self.position,
            "createBy": self.createBy,
            "createAt": self.createAt,
            "editBy": self.editBy,
            "editAt": self.editAt,
            "delBy": self.delBy,
            "delAt": self.delAt,
        }