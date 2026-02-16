def create_user(client, email="a@example.com", password="test1234"):
    r = client.post("/users", json={"email": email, "full_name": "A", "password": password})
    assert r.status_code == 200
    return r.json()

def login(client, email="a@example.com", password="test1234"):
    r = client.post("/users/login", json={"email": email, "password": password})
    assert r.status_code == 200
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_ticket_requires_auth(client):
    create_user(client)
    # no auth header
    r = client.post("/tickets", json={"title": "T1", "description": "D1"})
    assert r.status_code == 401  # Not authenticated

def test_owner_can_update_ticket(client):
    create_user(client, "a@example.com")
    headers = login(client, "a@example.com")

    r = client.post("/tickets", headers=headers, json={"title": "T1", "description": "D1"})
    assert r.status_code == 200
    ticket_id = r.json()["id"]

    r2 = client.patch(f"/tickets/{ticket_id}", headers=headers, json={"status": "resolved"})
    assert r2.status_code == 200
    assert r2.json()["status"] == "resolved"

def test_non_owner_cannot_update_ticket(client):
    # user A creates ticket
    create_user(client, "a@example.com")
    headers_a = login(client, "a@example.com")
    r = client.post("/tickets", headers=headers_a, json={"title": "T1", "description": "D1"})
    ticket_id = r.json()["id"]

    # user B tries to update
    create_user(client, "b@example.com")
    headers_b = login(client, "b@example.com")

    r2 = client.patch(f"/tickets/{ticket_id}", headers=headers_b, json={"status": "resolved"})
    assert r2.status_code == 403
