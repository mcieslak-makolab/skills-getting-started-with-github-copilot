from urllib.parse import quote


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_map(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload


def test_signup_adds_participant(client):
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "test.student@mergington.edu"

    response = client.post(f"/activities/{encoded_activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


def test_unregister_removes_participant(client):
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{encoded_activity_name}/participants", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants