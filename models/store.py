from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import Base

class Store(Base):
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True,nullable=False, unique=True)
    items=relationship("Item", back_populates="store",cascade="all, delete-orphan",passive_deletes=True,lazy="dynamic")
    tags=relationship("Tag", back_populates="store",cascade="all, delete-orphan",passive_deletes=True,lazy="dynamic")
    