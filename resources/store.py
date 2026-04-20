
from fastapi import FastAPI, HTTPException ,APIRouter,status,Depends
from sqlalchemy.orm import Session
from typing import List

#from pydantic import BaseModel
from db import get_db
import db
from models.user import User
from schemas.item import Item
from schemas.store import StoresResponse, StoresListResponse,StoreCreate
from models.store import Store 
from dependencies.auth import get_current_user

rt=APIRouter(tags=["stores"])


@rt.get('/store',status_code=status.HTTP_200_OK)
def get_all_stores(db: Session = Depends(get_db)):
    data=db.query(Store).all()
    result = []
    for store in data:
        result.append({
            "id": store.id,
            "name": store.name,
            "items": [
                {
                    "id": item.id,
                    "name": item.name,
                    "price": item.price
                }
                for item in store.items
            ],
            "tags": [
                {
                    "id": tag.id,
                    "name": tag.name
                }
                for tag in store.tags
            ]
        })

    return {
        "stores": result,
        "total": len(result)
    }

@rt.get("/store/{store_id}",status_code=status.HTTP_200_OK)
def get_store(store_id: int, db: Session = Depends(get_db)):
    
    store=db.get(Store, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    return {
        "id": store.id,
        "name": store.name,
        "items": [
            {"id": i.id, "name": i.name, "price": i.price}
            for i in store.items
        ],
        "tags": [
            {"id": t.id, "name": t.name}
            for t in store.tags
        ]
    }

@rt.post("/store", status_code=status.HTTP_201_CREATED)
def create_store(store: StoreCreate, db: Session = Depends(get_db),user: User = Depends(get_current_user)):
    existing = db.query(Store).filter(Store.name == store.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Store already exists")
    new_store = Store(name=store.name)
    db.add(new_store)
    db.commit()
    db.refresh(new_store)
    return {
        "id": new_store.id,
        "name": new_store.name,
        "items": [],
        "tags": []
    }

@rt.delete("/store/{store_id}",  status_code=status.HTTP_204_NO_CONTENT)
def delete_store(store_id: int, db:Session = Depends(get_db)):
    store=db.get(Store, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    items= [
            {"id": i.id, "name": i.name, "price": i.price}
            for i in store.items
        ]
    if items:
        raise HTTPException(status_code=400, detail="Store has items, cannot delete")
    
    db.delete(store)
    db.commit()
    return
