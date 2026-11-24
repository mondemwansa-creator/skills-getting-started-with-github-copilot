from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_signup_rejects_duplicate_email(monkeypatch):
    participants = []
    monkeypatch.setitem(activities["Chess Club"], "participants", participants)

    first_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "student@mergington.edu"},
    )
    duplicate_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert first_response.status_code == 200
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == (
        "Student is already signed up for this activity"
    )
    assert participants == ["student@mergington.edu"]
