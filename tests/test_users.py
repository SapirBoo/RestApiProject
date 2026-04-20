from tests.conftest import client, db_session
from models.user import User
from resources.user import send_email

def test_get_user(client, db_session):
    user=User(username="testuser", email="testuser@example.com", password="password123")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    response=client.get("/user/{user_id}".format(user_id=user.id))
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_delete_user(client, db_session):
    user=User(username="testuser2", email="testuser2@example.com", password="hashpassword")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    response=client.delete("/user/{user_id}".format(user_id=user.id))
    assert response.status_code == 200

def test_delete_nonexistent_user(client):
    response=client.delete("/user/9999")
    assert response.status_code == 404

def test_get_all_users(client, db_session):
    user1=User(username="user1", email="user1@example.com", password="password123")
    user2=User(username="user2", email="user2@example.com", password="password456")
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()
    db_session.refresh(user1)
    db_session.refresh(user2)

    response=client.get("/users")
    assert response.status_code == 200
    assert len(response.json()["users"]) == 2
    assert response.json()["users"][0]["name"] == "user1"
    assert response.json()["users"][1]["name"] == "user2"

def test_get_nonexistent_user(client):
    response=client.get("/user/9999")
    assert response.status_code == 404
    
    
def test_send_email_success(monkeypatch):
    from resources.user import send_email

    class MockResponse:
        status_code = 202
        body = b"ok"

    class MockSendGrid:
        def __init__(self, *args, **kwargs):
            pass

        def send(self, message):
            return MockResponse()

    monkeypatch.setattr(
        "resources.user.SendGridAPIClient",
        MockSendGrid
    )

    result = send_email("test@test.com", "Welcome")

    assert result["status_code"] == 202
    assert result["body"] == "ok"

def test_send_email_failure(monkeypatch):
    from resources.user import send_email

    class MockSendGrid:
        def __init__(self, *args, **kwargs):
            pass

        def send(self, message):
            raise Exception("Send failed")

    monkeypatch.setattr(
        "resources.user.SendGridAPIClient",
        MockSendGrid
    )


    result = send_email("test@test.com", "Welcome")

    assert "error" in result
    assert "Send failed" in result["error"]