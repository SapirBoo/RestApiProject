from models import item
from models.item import Item
from models.store import Store
from models.tag import Tag
from tests.conftest import db_session

def test_create_item_in_store(client, db_session):
    store=Store(name="Test Store2")
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)
    
    response=client.post("/item",json={
        "name":"TestItem2",
        "price": 12.99,
        "store_id": store.id
    })
    
    assert response.status_code == 201


def test_get_item(client, db_session):
    store=Store(name="Test Store2")
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)
    
    item=Item(name="TestItem2",price=19.99,store_id=store.id)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    response=client.get("/item/{item_id}".format(item_id=item.id))
    
    assert response.status_code == 200



def test_get_items_in_store(client, db_session):
    store=Store(name="Test Store3")
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)
    item=Item(name="TestItem3",price=14.99,store_id=store.id)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    response=client.get("/store/{store_id}/items".format(store_id=store.id))
    assert response.status_code == 200

def test_delete_item(client, db_session):
    store=Store(name="Test Store delete item")
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)
    item=Item(name="ItemDelete",price=9.99,store_id=store.id)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    response=client.delete("/item/{item_id}".format(item_id=item.id))
    assert response.status_code == 204
    
def test_get_invalid_item(client):
    response=client.get("/item/999")
    assert response.status_code == 404

def test_update_item(client, db_session):
    store=Store(name="Test Store update item")
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)
    item=Item(name="ItemUpdate",price=9.99,store_id=store.id)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    response=client.put("/item/{item_id}".format(item_id=item.id),json={
        "name":"UpdatedItem",
        "price": 15.99,
        "store_id": store.id
    })
    
    assert response.status_code == 200

def test_update_invalid_item(client):
    response=client.put("/item/999",json={
        "name":"UpdatedItem",
        "price": 15.99,
        "store_id": 1
    })
    assert response.status_code == 404
    
def test_link_item_to_tag(client, db_session):
   store=Store(name="Test Store link item to tag")
   db_session.add(store)
   db_session.commit()
   db_session.refresh(store)    
   
   item=Item(name="ItemLinkTag",price=9.99,store_id=store.id)
   db_session.add(item)
   db_session.commit()
   db_session.refresh(item)
   
   tag=Tag(name="TestTag",store_id=store.id)
   db_session.add(tag)
   db_session.commit()
   db_session.refresh(tag)
   
   response=client.post("/tags/{tag_id}/item/{item_id}".format(tag_id=tag.id,item_id=item.id))
   assert response.status_code == 200
   
def test_link_item_to_nonexistent_tag(client, db_session):
    store=Store(name="Test Store link item to non-existent tag")
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)    
    
    item=Item(name="ItemLinkNonExistentTag",price=9.99,store_id=store.id)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    response=client.post("/tags/999/item/{item_id}".format(item_id=item.id))
    assert response.status_code == 404

def test_remove_item_from_tag(client, db_session):
    store=Store(name="Test Store remove item from tag")
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)    
    
    item=Item(name="ItemRemoveFromTag",price=9.99,store_id=store.id)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    tag=Tag(name="TestTagRemove",store_id=store.id)
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)
    
    client.post("/tags/{tag_id}/item/{item_id}".format(tag_id=tag.id,item_id=item.id))
    
    response=client.delete("/tags/{tag_id}/items/{item_id}".format(tag_id=tag.id,item_id=item.id))
    assert response.status_code == 200

def test_remove_item_from_nonexistent_tag(client, db_session):
    store=Store(name="Test Store remove item from non-existent tag")
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)    
    
    item=Item(name="ItemRemoveFromNonExistentTag",price=9.99,store_id=store.id)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    response=client.delete("/tags/999/items/{item_id}".format(item_id=item.id))
    assert response.status_code == 404