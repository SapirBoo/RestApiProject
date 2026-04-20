
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException ,APIRouter,status,Depends
from sqlalchemy.orm import Session
from typing import List

from db import get_db
import db
from models.store import Store
from models.tag import Tag
from schemas.item import ItemCreate, ItemUpdate,ItemResponse,Item, ItemsListResponse
from models.item import Item 


rt=APIRouter( tags=["stores"])

@rt.get("/items", status_code=status.HTTP_200_OK)
def get_items(db: Session = Depends(get_db)):
    data=db.query(Item).all()
    return {
        "items": [
            {"id": i.id, "name": i.name, "price": i.price}
            for i in data
        ],
        "total": len(data),
        "message": None if data else "No items found"
    }

@rt.get("/item/{item_id}", status_code=status.HTTP_200_OK)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "store_id":item.store_id
    }

@rt.post("/item", status_code=status.HTTP_201_CREATED)
def create_item_in_store(new_item: ItemCreate, db: Session = Depends(get_db)):    
    storeExisting = db.query(Store).filter(Store.id == new_item.store_id).first()
    if not storeExisting:
        raise HTTPException(status_code=404, detail="Store not found")
    
    item= Item(name=new_item.name,price=new_item.price,store_id=new_item.store_id)   
    db.add(item)
    db.commit()
    db.refresh(item)
    return {
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "store_id":item.store_id
    }

@rt.get("/store/{store_id}/items",status_code=status.HTTP_200_OK)
def get_items_in_store(store_id: int,db: Session=Depends(get_db)):
    data = db.query(Item).filter(Item.store_id == store_id).all()
    return {
        "items": [
            {"id": i.id, "name": i.name, "price": i.price,"store_id":i.store_id}
            for i in data
        ],
        "total": len(data),
        "message": None if data else "No items found"
    }

@rt.delete("/item/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id:int,db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return

@rt.put("/item/{item_id}", status_code=status.HTTP_200_OK)
def update_item(item_id:int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item=db.query(Item).filter(Item.id==item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    update_item= item.model_dump(exclude_unset=True)
    
    #Validation on Price
    if "price" in update_item and update_item["price"] <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than 0")
    
    for key, value in update_item.items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)

    return {
        "id": db_item.id,
        "name": db_item.name,
        "price": db_item.price,
        "store_id":db_item.store_id
    }

@rt.post("/tags/{tag_id}/item/{item_id}",status_code=status.HTTP_200_OK)
def linkItemToTag(item_id: int,tag_id : int,db: Session=Depends(get_db)):
    item = db.get(Item, item_id)
    tag= db.get(Tag, tag_id)
    if not item or not tag:
        raise HTTPException(status_code=404, detail="Tag or Item not found")
    
    tag.items.append(item)
    
    db.add(tag)
    db.commit()
    db.refresh(item)
    return {
        "id": item.id,
        "name": item.id,
        "price": item.price,
        "tags": [
            {"id": t.id, "name": t.name}
            for t in item.tags
        ]
    }


@rt.delete("/tags/{tag_id}/items/{item_id}",status_code=status.HTTP_200_OK)
def removeItemFromTag(tag_id: int, item_id: int,db: Session = Depends(get_db)):
    tag = db.get(Tag, tag_id)
    item = db.get(Item, item_id)

    if not tag or not item:
        raise HTTPException(status_code=404, detail="Tag or Item not found")
    
    if tag not in item.tags:
        return {"message": "Tag not attached to item"}

    tag.items.remove(item)
    db.commit()
    return {"message": "Tag removed from item"}