from models.tag import Tag
from models.itams_tags import items_tags
from models.item import Item
from models.store import Store
from tests.conftest import db_session

def test_create_tag_in_store(client, db_session):
    store=Store(name="Test Store for Tag")
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)
    
    response=client.post("/store/tag",json={
        "name":"TestTag1",
        "store_id": store.id
    })
    
    assert response.status_code == 201
    assert response.json()["name"] == "TestTag1"
    assert response.json()["store_id"] == store.id


def test_create_tag_in_nonexistent_store(client):
    response=client.post("/store/tag",json={
        "name":"TestTag1",
        "store_id": 9999
    })
    assert response.status_code == 404
    
def test_get_tags_in_store(client, db_session):
    store=Store(name="storeTestGetTags")
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)
    tag=Tag(name="TestTag3",store_id=store.id)
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)
    
    response=client.get("/store/{store_id}/tags".format(store_id=store.id))
    print(f"Response= {response.json()}")
    assert response.status_code == 200
    assert (response.json()["total"]) == 1

def test_get_tags_in_nonexistent_store(client, db_session):
    response=client.get("/store/9999/tags")
    assert response.status_code == 404

def test_delete_tag(client, db_session):
   store=Store(name="store for delete tag")
   db_session.add(store)
   db_session.commit()
   db_session.refresh(store)
   
   tag=Tag(name="Tag to delete",store_id=store.id)
   db_session.add(tag)
   db_session.commit()
   db_session.refresh(tag)
   
   response=client.delete("/tag/{tag_id}".format(tag_id=tag.id))
   assert response.status_code == 204
   
def test_delete_nonexistent_tag(client):
    response=client.delete("/tag/9999")
    assert response.status_code == 404

def test_link_tag_to_item(client, db_session):
   store=Store(name="store for link tag to item")
   db_session.add(store)
   db_session.commit()
   db_session.refresh(store)
   item=Item(name="Item for tag link",price=5.99,store_id=store.id)
   db_session.add(item)
   db_session.commit()
   db_session.refresh(item)
   
   tag=Tag(name="Tag for item link",store_id=store.id)
   db_session.add(tag)
   db_session.commit()
   db_session.refresh(tag)
   
   response=client.post("/item/{item_id}/tag/{tag_id}".format(item_id=item.id, tag_id=tag.id))
   
   assert response.status_code == 200

def test_link_tag_to_nonexistent_item(client, db_session):
   store=Store(name="store for link tag to non existent item")
   db_session.add(store)
   db_session.commit()
   db_session.refresh(store)
   
   tag=Tag(name="Tag for non existent item link",store_id=store.id)
   db_session.add(tag)
   db_session.commit()
   db_session.refresh(tag)
   
   response=client.post("/item/9999/tag/{tag_id}".format(tag_id=tag.id))
   
   assert response.status_code == 404

def test_link_nonexistent_tag_to_item(client, db_session):
   store=Store(name="store for link non existent tag to item")
   db_session.add(store)
   db_session.commit()
   db_session.refresh(store)
   item=Item(name="Item for non existent tag link",price=5.99,store_id=store.id)
   db_session.add(item)
   db_session.commit()
   db_session.refresh(item)
   
   response=client.post("/item/{item_id}/tag/9999".format(item_id=item.id))
   
   assert response.status_code == 404

def test_remove_tag_from_item(client, db_session):
   store=Store(name="store for remove tag from item")
   db_session.add(store)
   db_session.commit()
   db_session.refresh(store)
   
   item=Item(name="Item for remove tag link",price=5.99,store_id=store.id)
   db_session.add(item)
   db_session.commit()
   db_session.refresh(item)
   
   tag=Tag(name="Tag for remove item link",store_id=store.id)
   db_session.add(tag)
   db_session.commit()
   db_session.refresh(tag)
   
   client.post("/item/{item_id}/tag/{tag_id}".format(item_id=item.id, tag_id=tag.id))
   
   response=client.delete("/{tag_id}/items/{item_id}".format(tag_id=tag.id,item_id=item.id))
   
   assert response.status_code == 200

def test_remove_tag_from_nonexistent_item(client, db_session):
   store=Store(name="store for remove non existent tag from item")
   db_session.add(store)
   db_session.commit()
   db_session.refresh(store)
   
   item=Item(name="Item for remove non existent tag link",price=5.99,store_id=store.id)
   db_session.add(item)
   db_session.commit()
   db_session.refresh(item)
   
   tag=Tag(name="Tag for remove non existent tag link",store_id=store.id)
   db_session.add(tag)
   db_session.commit()
   db_session.refresh(tag)
   
   client.post("/item/{item_id}/tag/{tag_id}".format(item_id=item.id, tag_id=tag.id))
   response=client.delete("/{tag_id}/items/9999".format(tag_id=tag.id))
   
   assert response.status_code == 404
   
def test_remove_tag_not_linked_to_item(client, db_session):
    store=Store(name="store for remove tag not linked to item")
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)
    
    item=Item(name="Item for remove tag not linked to item",price=5.99,store_id=store.id)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    tag=Tag(name="Tag for remove tag not linked to item",store_id=store.id)
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)
    
    response=client.delete("/{tag_id}/items/{item_id}".format(tag_id=tag.id,item_id=item.id))
    
    assert response.status_code == 400