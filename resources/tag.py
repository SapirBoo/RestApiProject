
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException ,APIRouter,status,Depends
from sqlalchemy.orm import Session
from typing import List

from db import get_db
import db
from models.store import Store
from schemas.tag import TagCreate,TagResponse,Tag, TagListResponse
from models.item import Item 
from models.tag import Tag

rt=APIRouter( tags=["tags"])

@rt.get("/store/{store_id}/tags",status_code=status.HTTP_200_OK)
def get_tags_in_store(store_id: int,db: Session=Depends(get_db)):
    data= db.query(Tag).filter(Tag.store_id == store_id).all()
    return {
        "tags":[
            {"id": i.id, "name": i.name, "store_id": i.store_id}
            for i in data
        ],
        "total": len(data),
        "message": None if data else "No tags found"
    }
    

@rt.get("/tags/{tag_id}",status_code=status.HTTP_200_OK)
def get_tag(tag_id: int,db: Session=Depends(get_db)):
    tag= db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {
        "id": tag.id,
        "name": tag.name
    }

@rt.post("/store/tag",status_code=status.HTTP_201_CREATED)
def create_tag(new_tag: TagCreate,db: Session=Depends(get_db)):
    storeExisting = db.query(Store).filter(Store.id == new_tag.store_id).first()
    if not storeExisting:
        raise HTTPException(status_code=404, detail="Store not found")
    tag= Tag(name=new_tag.name,store_id=new_tag.store_id)   
    db.add(tag)
    db.commit()
    db.refresh(tag)
    
    return {
        "id": tag.id,
        "name": tag.name,
        "store_id": tag.store_id
    }


@rt.post("/item/{item_id}/tag/{tag_id}",status_code=status.HTTP_200_OK)
def linkTagToItem(item_id: int,tag_id : int,db: Session=Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    tag= db.query(Tag).filter(Tag.id == tag_id).first()
    if not item or not tag:
        raise HTTPException(status_code=404, detail="Tag or Item not found")
    
    item.tags.append(tag)
    
    db.add(item)
    db.commit()
    db.refresh(tag)
    return {
        "id": item.id,
        "name": item.id,
        "price": item.price,
        "items": [
            {"id": i.id, "name": i.name, "price": i.price}
            for i in tag.items
        ],
    }


@rt.delete("/tag/{tag_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_item(tag_id:int ,db: Session = Depends(get_db)):
    tag=db.query(Tag).filter(tag_id ==Tag.id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    db.delete(tag)
    db.commit()
    return  

@rt.delete("/{tag_id}/items/{item_id}",status_code=status.HTTP_200_OK)
def removeTagFromItem(tag_id: int, item_id: int,db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(tag_id ==Tag.id).first()
    item = db.query(Item).filter(Item.id == item_id).first()

    if not tag or not item:
        raise HTTPException(status_code=404, detail="Tag or Item not found")
    
    if tag not in item.tags:
        return {"message": "Tag not attached to item"}

    item.tags.remove(tag)
    db.commit()
    return {"message": "Tag removed from item"}