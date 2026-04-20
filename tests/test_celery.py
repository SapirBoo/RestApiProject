import pytest
from tasks import send_verification_email

def test_send_email_success(monkeypatch):
    class MockResponse:
        status_code = 202

    class MockSendGrid:
        def __init__(self, *args, **kwargs):
            pass

        def send(self, message):
            return MockResponse()
    monkeypatch.setattr(
        "tasks.SendGridAPIClient",
        MockSendGrid
    )

    result = send_verification_email(
        "test@test.com",
        "testuser",
        "token123"
    )

    assert result == 202    

def test_send_email_failure(monkeypatch):
    class MockSendGrid:
        def __init__(self, *args, **kwargs):
            pass

        def send(self, message):
            raise Exception("Send failed")

    monkeypatch.setattr(
        "tasks.SendGridAPIClient",
        MockSendGrid
    )

    result = send_verification_email(
        "test@test.com",
        "testuser",
        "token123"
    )

    assert "Send failed" in result
    
def test_send_email_payload(monkeypatch):
    
    captured = {}
    
    class MockSendGrid:
        def __init__(self, *args, **kwargs):
            pass
        def send(self, message):
            captured["message"] = message
            return type("Res", (), {"status_code": 202})()
    monkeypatch.setattr(
        "tasks.SendGridAPIClient",
        MockSendGrid
    )
    
    send_verification_email(
        "test@test.com",
        "testuser",
        "token123"
    )
    
    message = captured["message"]
    data=message.personalizations[0].dynamic_template_data

    assert data["email"] == "test@test.com"
    assert data["name"] == "testuser"
    assert "token123" in data["verification_link"]
