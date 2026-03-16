from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Test POST signup
def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.delete(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

# Test DELETE participant
def test_delete_participant():
    email = "testdelete@mergington.edu"
    activity = "Programming Class"
    # Ensure participant exists
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"
    # Deleting again should fail
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

# Test activity not found
def test_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404
    response = client.delete("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404

# Test GET root redirects
def test_root_redirect():
    response = client.get("/")
    assert response.status_code in (200, 307, 308)
