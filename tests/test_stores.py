from models.store import Store
from models.item import Item
from models.tag import Tag
from models.user import User
from tests.conftest import client
from tests.conftest import db_session
from tests.utils.jwt_utils import create_valid_token
from conftest import SQLALCHEMY_DATABASE_URL

def test_create_store(client, db_session):
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "password123"
    })
    user=db_session.query(User).filter(User.username == "testuser").first()
    user.is_verified=True
    db_session.commit()
    db_session.refresh(user)
    
    token = create_valid_token(user.id)
    client.get("/verify", params={"token": token})

    responseLogin=client.post("/login",json={
        "username":"testuser",
        "password":"password123"
     })
    
    client.headers.update({"Authorization": f"Bearer {responseLogin.json()['access_token']}"})
    response = client.post("/store", json={"name": "Test Store"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Store"

def test_create_duplicate_store(client, db_session):
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "password123"
    })
    user=db_session.query(User).filter(User.username == "testuser").first()
    user.is_verified=True
    db_session.commit()
    db_session.refresh(user)
    
    token = create_valid_token(user.id)
    client.get("/verify", params={"token": token})
    
    responseLogin=client.post("/login",json={
        "username":"testuser",
        "password":"password123"
     })
    
    store=Store(name="Test Store Duplicate")
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)
    
    client.headers.update({"Authorization": f"Bearer {responseLogin.json()['access_token']}"})
    response=client.post("/store", json={"name": "Test Store Duplicate"})  
    
    assert response.status_code == 400  

def test_get_store(client, db_session):
    store=Store(name="test store get")
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)
    
    response=client.get("/store/{store_id}".format(store_id=store.id))
    
    assert response.status_code == 200
    assert response.json()["name"] == "test store get"


def test_delete_store(client, db_session):
    store=Store(name="Test Store Delete")
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)
    
    response=client.delete("/store/{store_id}".format(store_id=store.id))
    
    assert response.status_code == 204

def test_delete_nonexistent_store(client):
    response=client.delete("/store/9999")
    assert response.status_code == 404

def test_delete_store_with_items(client, db_session):
   store=Store(name="Store With Items")
   db_session.add(store)
   db_session.commit()
   db_session.refresh(store)
   
   item=Item(name="Item in store",price=8.90,store_id=store.id)
   db_session.add(item)
   db_session.commit()
   db_session.refresh(item)
   
   response=client.delete("/store/{store_id}".format(store_id=store.id))
   assert response.status_code == 400

def test_create_store_with_wrong_DB_url(client):
   SQLALCHEMY_DATABASE_URL = "postgresql://wrong_user:wrong_password@localhost:5432/wrong_db"
   response=client.post("/store", json={"name": "Store With Wrong DB"})
   assert response.status_code == 401
   

def test_create_store_with_item(client,db_session):
    store=Store(name="Store With Item")
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)
    
    item=Item(name="Item in store",price=8.90,store_id=store.id)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    store2=Store(name="Store2 With Item")
    db_session.add(store2)
    db_session.commit()
    db_session.refresh(store2)
    
    tag=Tag(name="Tag for item",store_id=store.id)
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)
    client.post("/tags/{tag_id}/item/{item_id}".format(tag_id=tag.id,item_id=item.id))
    response=client.get("/store", params={})
    
    data = response.json()["stores"]

    names = [s["name"] for s in data]
    store_data = next(s for s in data if s["name"] == "Store With Item")

    assert "Store With Item" in names
    assert "Store2 With Item" in names
    assert len(data) == 2

    assert len(store_data["tags"]) >= 1    
    assert len(store_data["items"]) >= 1
    
def test_get_nonexistent_store(client):
    response=client.get("/store/9999")
    assert response.status_code == 404