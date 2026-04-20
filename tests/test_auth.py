

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.user import User
from schemas import user
from tests.conftest import db_session
from tests.utils.jwt_utils  import create_invalid_token, create_token_with_wrong_secret, create_valid_token

def test_register(client: TestClient):
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "123456"
    })

    assert response.status_code == 201
    assert response.json()["msg"] == "User created successfully"
    
def test_login_not_verified(client: TestClient):
    client.post("/register", json={
        "username": "user2",
        "email": "user2@test.com",
        "password": "123456"
        
    })
    
    response = client.post("/login", json={
        "username": "user2",
        "password": "123456"
    })
    print(f"Rsponse= {response.json()}")
    
    assert response.status_code == 403


def test_verify_email(client: TestClient, db_session: Session):
    # create user directly
    user = User(
        username="verifyuser",
        email="verify@test.com",
        password="hashed",
        is_verified=False
    )
    db_session.add(user)
    db_session.commit()
    
    db_session.refresh(user)

    token = create_valid_token(user.id)

    response = client.get("/verify", params={"token": token})
    
    assert response.status_code == 200


def test_login_verified(client: TestClient, db_session: Session):
    client.post("/register", json={
        "username": "user4",
        "email": "user4@test.com",
        "password": "123456"
        
    })
    db_session.query(User).filter(User.username == "user4").update({"is_verified": True})
    db_session.commit()
    db_session.refresh(db_session.query(User).filter(User.username == "user4").first())
    
    response_login=client.post("/login",json={
        "username":"user4",
        "password":"123456"
    })
    assert response_login.status_code == 200

def test_verify_invalid_token(client: TestClient):
    client.post("/register", json={
        "username": "user5",
        "email": "user5@test.com",
        "password": "hashhash"
        
    })
    response = client.get("/verify", params={"token": "invalid"})
    
    assert response.status_code == 400


def test_verify_twice(client: TestClient, db_session: Session):
    user = User(
        username="verifyTwiceUser",
        email="verifyTwiceUser@test.com",
        password="hashed",
        is_verified=False
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    response=client.get("/verify", params={"token": create_valid_token(user.id)})
    response2=client.get("/verify",params={"token":create_valid_token(user.id)})
    
    assert response2.status_code == 200

def test_register_duplicate_username(client: TestClient):
    client.post("/register", json={
        "username": "duplicateuser",
        "email": "duplicateuser@test.com",
        "password": "123456"
    })
    response = client.post("/register", json={
        "username": "duplicateuser",
        "email": "duplicateuser2@test.com",
        "password": "123456"
    })
    assert response.status_code == 400

def test_register_duplicate_email(client: TestClient):
    client.post("/register", json={
        "username": "uniqueuser",
        "email": "uniqueuser@test.com",
        "password": "123456"
    })
    response = client.post("/register", json={
        "username": "uniqueuser2",
        "email": "uniqueuser@test.com",
        "password": "123456"
    })
    assert response.status_code == 400
    
def test_user_login_wrong_password(client: TestClient, db_session: Session):
    client.post("/register", json={
        "username": "wrongpassuser",
        "email": "wrongpassuser@test.com",
        "password": "123456"
    })
    response = client.post("/login", json={
        "username": "wrongpassuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_refresh_token(client: TestClient, db_session: Session):
    client.post("/register", json={
        "username": "refreshuser",
        "email": "refreshuser@test.com",
        "password": "123456"
    })
    db_session.query(User).filter(User.username == "refreshuser").update({"is_verified": True})
    db_session.commit()
    db_session.refresh(db_session.query(User).filter(User.username == "refreshuser").first())
    
    response_login=client.post("/login",json={
        "username":"refreshuser",
        "password":"123456"})
    
    refresh_token=response_login.json().get("refresh_token")
    client.headers.update({"Authorization": f"Bearer {refresh_token}"})
    response_refresh=client.post("/refresh",json={})
    assert response_refresh.status_code == 200
    assert "access_token" in response_refresh.json()
    

def test_logout_user(client: TestClient, db_session: Session):
    client.post("/register", json={
        "username": "logoutuser",
        "email": "logoutuser@test.com",
        "password": "123456"
    })
    db_session.query(User).filter(
        User.username == "logoutuser").update({"is_verified": True})
    db_session.commit()
    db_session.refresh(db_session.query(User).filter(User.username == "logoutuser").first())
    
    response_login=client.post("/login",json={
        "username":"logoutuser",
        "password":"123456"})
    
    access_token=response_login.json().get("access_token")
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    response_logout=client.post("/logout")
    assert response_logout.status_code == 200
    

def test_access_protected_route_after_logout(client: TestClient, db_session: Session):
    client.post("/register", json={
        "username": "protecteduser",
        "email": "protecteduser@test.com",
        "password": "123456"
    })
    db_session.query(User).filter(User.username == "protecteduser").update({"is_verified": True})
    db_session.commit()
    db_session.refresh(db_session.query(User).filter(User.username == "protecteduser").first())

    response_login=client.post("/login",json={
        "username":"protecteduser",
        "password":"123456"})
    
    access_token=response_login.json().get("access_token")
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    response_logout=client.post("/logout")
    
    response_login_after_logout=client.get("/protected")
    assert response_login_after_logout.status_code == 401

    
def test_logout_invalid_token(client):  
    client.headers.update({"Authorization": f"Bearer {create_invalid_token()}"})
    response = client.post("/logout",json={})
    print(f"Response for invalid token: {response.json()}")
    assert response.status_code == 401

def test_refresh_invalid_token(client,db_session):
    client.post("/register", json={
        "username": "refreshinvaliduser",
        "email": "refreshinvaliduser@test.com",
        "password": "123456"
    })
    
    db_session.query(User).filter(User.username == "refreshinvaliduser").update({"is_verified": True})
    db_session.commit()
    db_session.refresh(db_session.query(User).filter(User.username == "refreshinvaliduser").first())
    response_login = client.post("/login", json={
        "username": "refreshinvaliduser",
        "password": "123456"
    })
    user=db_session.query(User).filter(User.username == "refreshinvaliduser").first()
    access_token=create_token_with_wrong_secret(user.id)
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    response_logout=client.post("/logout",json={})
    print(f"Response for refresh after logout: {response_logout.json()}")
    assert response_logout.status_code == 401