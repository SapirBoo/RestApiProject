from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from .itams_tags import items_tags

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False, unique=True,index=True)
    price = Column(Integer, nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)
    store = relationship("Store", back_populates="items")
    tags= relationship("Tag", back_populates="items",secondary=items_tags)