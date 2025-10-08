def test_print_routes():
    print("\nRegistered routes:")
    for route in app.routes:
        if hasattr(route, 'methods'):
            print(f"{route.path} [{route.methods}] -> {route.endpoint}")
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Signed up")
    # Clean up
    client.post(f"/activities/{activity}/unregister?email={email}")


def test_unregister_from_activity():
    email = "removeme@mergington.edu"
    activity = "Chess Club"
    # Add first
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Removed")


def test_signup_duplicate():
    email = "duplicate@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Clean up
    client.post(f"/activities/{activity}/unregister?email={email}")


def test_unregister_nonexistent():
    email = "notfound@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]
